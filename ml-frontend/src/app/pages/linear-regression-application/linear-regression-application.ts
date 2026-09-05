import { CurrencyPipe, DecimalPipe } from '@angular/common';
import { Component, OnInit, computed, inject, signal } from '@angular/core';
import { FormBuilder, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { LinearRegressionService } from '../../services/linear-regression.service';
import { SalaryRecord } from '../../models/salary-data.model';
import { ModelInfo, SalaryPredictionResponse } from '../../models/salary-prediction.model';

@Component({
  selector: 'app-linear-regression-application',
  imports: [FormsModule, ReactiveFormsModule, RouterLink, CurrencyPipe, DecimalPipe],
  templateUrl: './linear-regression-application.html',
})
export class LinearRegressionApplication implements OnInit {
  private readonly linearRegressionService = inject(LinearRegressionService);
  private readonly formBuilder = inject(FormBuilder);

  // --- Model + prediction state ---
  public modelInfo = signal<ModelInfo | null>(null);
  public prediction = signal<SalaryPredictionResponse | null>(null);
  public loading = signal(false);
  public errorMessage = signal<string | null>(null);

  public readonly presets = [1, 3, 5, 10, 15, 20, 25];
  public plotUrl = signal<string>(this.linearRegressionService.regressionPlotUrl());

  public form = this.formBuilder.group({
    years: [
      null as number | null,
      [Validators.required, Validators.pattern(/^\d+(\.\d+)?$/), Validators.min(0), Validators.max(80)],
    ],
  });

  // --- Data table state ---
  limitOptions = [10, 20, 50, 100, 500];
  limit = 20;
  page = signal(1);
  totalPages = signal(1);
  totalRecords = signal(0);
  records = signal<SalaryRecord[]>([]);
  tableLoading = signal(false);

  public readonly rangeStart = computed(() =>
    this.totalRecords() === 0 ? 0 : (this.page() - 1) * this.limit + 1,
  );
  public readonly rangeEnd = computed(() =>
    Math.min(this.page() * this.limit, this.totalRecords()),
  );

  ngOnInit(): void {
    this.linearRegressionService.getModelInfo().subscribe({
      next: (info) => this.modelInfo.set(info),
      error: () => {
        /* stats card simply stays hidden if this fails */
      },
    });
    this.fetchSalaryData();
  }

  // --- Prediction ---
  public usePreset(value: number): void {
    this.form.patchValue({ years: value });
    this.predictSalary();
  }

  public clearPrediction(): void {
    this.form.reset();
    this.prediction.set(null);
    this.errorMessage.set(null);
    this.plotUrl.set(this.linearRegressionService.regressionPlotUrl());
  }

  public predictSalary(): void {
    this.form.markAllAsTouched();
    if (this.form.invalid) {
      return;
    }

    const years = Number(this.form.value.years);
    this.loading.set(true);
    this.errorMessage.set(null);

    this.linearRegressionService.calculateSalaryPrediction(years).subscribe({
      next: (response) => {
        this.prediction.set(response);
        this.plotUrl.set(this.linearRegressionService.regressionPlotUrl(years));
        this.loading.set(false);
      },
      error: () => {
        this.errorMessage.set('Something went wrong while contacting the model. Please try again.');
        this.loading.set(false);
      },
    });
  }

  public get yearsControl() {
    return this.form.get('years');
  }

  // --- Data table ---
  fetchSalaryData(): void {
    this.tableLoading.set(true);
    this.linearRegressionService.getSalaryData(this.page(), this.limit).subscribe({
      next: (response) => {
        this.records.set(response.records);
        this.page.set(response.page);
        this.totalPages.set(response.totalPages);
        this.totalRecords.set(response.totalRecords);
        this.tableLoading.set(false);
      },
      error: () => this.tableLoading.set(false),
    });
  }

  onLimitChange(): void {
    this.page.set(1);
    this.fetchSalaryData();
  }

  goToPreviousPage(): void {
    if (this.page() > 1) {
      this.page.set(this.page() - 1);
      this.fetchSalaryData();
    }
  }

  goToNextPage(): void {
    if (this.page() < this.totalPages()) {
      this.page.set(this.page() + 1);
      this.fetchSalaryData();
    }
  }
}
