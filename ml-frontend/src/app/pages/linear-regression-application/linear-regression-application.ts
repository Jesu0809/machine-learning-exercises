import { Component, OnInit, inject, signal } from '@angular/core';
import { FormBuilder, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { LinearRegressionService } from '../../services/linear-regression.service';
import { SalaryRecord } from '../../models/salary-data.model';

@Component({
  selector: 'app-linear-regression-application',
  imports: [FormsModule, ReactiveFormsModule, RouterLink],
  templateUrl: './linear-regression-application.html'
})
export class LinearRegressionApplication implements OnInit {
  public result = signal<number | null>(null);
  public loading = signal(false);
  public errorMessage = signal<string | null>(null);

  limitOptions = [10, 20, 50, 100, 500];
  limit = 20;
  page = signal(1);
  totalPages = signal(1);
  totalRecords = signal(0);
  records = signal<SalaryRecord[]>([]);
  tableLoading = signal(false);

  private readonly linearRegressionService = inject(LinearRegressionService);
  private readonly formBuilder = inject(FormBuilder);

  public form = this.formBuilder.group({
    years: [null as number | null, [Validators.required, Validators.pattern(/^\d+(\.\d+)?$/), Validators.min(0)]]
  });

  ngOnInit() {
    this.fetchSalaryData();
  }

  public predictSalary(): void {
    this.form.markAllAsTouched();

    if (this.form.invalid) {
      return;
    }

    const years = this.form.value.years as number;

    this.loading.set(true);
    this.errorMessage.set(null);
    this.result.set(null);

    this.linearRegressionService.calculateSalaryPrediction(years)
      .subscribe({
        next: (response) => {
          this.result.set(response.result);
          this.loading.set(false);
        },
        error: () => {
          this.errorMessage.set('Something went wrong. Please try again.');
          this.loading.set(false);
        }
      });
  }

  fetchSalaryData() {
    this.tableLoading.set(true);
    this.linearRegressionService.getSalaryData(this.page(), this.limit)
      .subscribe({
        next: (response) => {
          this.records.set(response.records);
          this.page.set(response.page);
          this.totalPages.set(response.totalPages);
          this.totalRecords.set(response.totalRecords);
          this.tableLoading.set(false);
        },
        error: () => {
          this.tableLoading.set(false);
        }
      });
  }

  onLimitChange() {
    this.page.set(1);
    this.fetchSalaryData();
  }

  goToPreviousPage() {
    if (this.page() > 1) {
      this.page.set(this.page() - 1);
      this.fetchSalaryData();
    }
  }

  goToNextPage() {
    if (this.page() < this.totalPages()) {
      this.page.set(this.page() + 1);
      this.fetchSalaryData();
    }
  }
}
