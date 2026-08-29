import { Component, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { SalaryPredictionResponse } from '../../models/salary-prediction.model';

@Component({
  selector: 'app-linear-regression',
  imports: [FormsModule],
  templateUrl: './linear-regression.html',
  styleUrl: './linear-regression.css'
})
export class LinearRegression {
  years: number | null = null;
  result = signal<number | null>(null);
  loading = signal(false);
  errorMessage = signal<string | null>(null);

  constructor(private http: HttpClient) {}

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
}