import { DecimalPipe, PercentPipe } from '@angular/common';
import { Component, OnInit, computed, inject, signal } from '@angular/core';
import { FormBuilder, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { LogisticRegressionService } from '../../services/logistic-regression.service';
import { LogRegInfo, LogRegRecord, LogRegResult } from '../../models/classification.model';

@Component({
  selector: 'app-logistic-regression-application',
  imports: [FormsModule, ReactiveFormsModule, RouterLink, DecimalPipe, PercentPipe],
  templateUrl: './logistic-regression-application.html',
})
export class LogisticRegressionApplication implements OnInit {
  private readonly service = inject(LogisticRegressionService);
  private readonly formBuilder = inject(FormBuilder);

  public modelInfo = signal<LogRegInfo | null>(null);
  public result = signal<LogRegResult | null>(null);
  public loading = signal(false);
  public errorMessage = signal<string | null>(null);
  public plotUrl = signal<string>(this.service.scatterPlotUrl());

  public readonly presets = [10, 20, 30, 40, 50, 60];

  public form = this.formBuilder.group({
    ratio: [
      null as number | null,
      [
        Validators.required,
        Validators.pattern(/^\d+(\.\d+)?$/),
        Validators.min(0),
        Validators.max(100),
      ],
    ],
  });

  limitOptions = [10, 20, 50, 100];
  limit = 20;
  page = signal(1);
  totalPages = signal(1);
  totalRecords = signal(0);
  records = signal<LogRegRecord[]>([]);
  tableLoading = signal(false);

  public readonly rangeStart = computed(() =>
    this.totalRecords() === 0 ? 0 : (this.page() - 1) * this.limit + 1,
  );
  public readonly rangeEnd = computed(() =>
    Math.min(this.page() * this.limit, this.totalRecords()),
  );

  ngOnInit(): void {
    this.service.getModelInfo().subscribe({
      next: (info) => this.modelInfo.set(info),
      error: () => {},
    });
    this.fetchData();
  }

  public get ratioControl() {
    return this.form.get('ratio');
  }

  public usePreset(value: number): void {
    this.form.patchValue({ ratio: value });
    this.classify();
  }

  public classify(): void {
    this.form.markAllAsTouched();
    if (this.form.invalid) {
      return;
    }
    const ratio = Number(this.form.value.ratio);
    this.loading.set(true);
    this.errorMessage.set(null);

    this.service.classify(ratio).subscribe({
      next: (response) => {
        this.result.set(response);
        this.plotUrl.set(this.service.scatterPlotUrl(ratio));
        this.loading.set(false);
      },
      error: () => {
        this.errorMessage.set(
          'Something went wrong while contacting the model. Please try again.',
        );
        this.loading.set(false);
      },
    });
  }

  public clear(): void {
    this.form.reset();
    this.result.set(null);
    this.errorMessage.set(null);
    this.plotUrl.set(this.service.scatterPlotUrl());
  }

  fetchData(): void {
    this.tableLoading.set(true);
    this.service.getDataset(this.page(), this.limit).subscribe({
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
    this.fetchData();
  }

  previousPage(): void {
    if (this.page() > 1) {
      this.page.set(this.page() - 1);
      this.fetchData();
    }
  }

  nextPage(): void {
    if (this.page() < this.totalPages()) {
      this.page.set(this.page() + 1);
      this.fetchData();
    }
  }
}
