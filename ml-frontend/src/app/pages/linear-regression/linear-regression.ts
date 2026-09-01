import { Component, OnInit, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { SalaryPredictionResponse } from '../../models/salary-prediction.model';
import { SalaryDataResponse, SalaryRecord } from '../../models/salary-data.model';

@Component({
  selector: 'app-linear-regression',
  imports: [FormsModule],
  templateUrl: './linear-regression.html',
  styleUrl: './linear-regression.css'
})
export class LinearRegression implements OnInit {
  years: number | null = null;
  result = signal<number | null>(null);
  loading = signal(false);
  errorMessage = signal<string | null>(null);

  limitOptions = [2, 5, 10, 20, 50, 100, 500];
  limit = 20;
  page = signal(1);
  totalPages = signal(1);
  totalRecords = signal(0);
  records = signal<SalaryRecord[]>([]);
  tableLoading = signal(false);

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.fetchSalaryData();
  }

  predictSalary() {
    if (this.years === null) {
      return;
    }
    this.loading.set(true);
    this.errorMessage.set(null);
    this.result.set(null);

    this.http.post<SalaryPredictionResponse>('/api/predict-salary', { years: this.years })
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
    this.http.get<SalaryDataResponse>(`/api/salary-data?page=${this.page()}&limit=${this.limit}`)
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