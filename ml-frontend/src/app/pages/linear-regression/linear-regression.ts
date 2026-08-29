import { Component, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { GradePredictionResponse } from '../../models/grade-prediction.model';

@Component({
  selector: 'app-linear-regression',
  imports: [FormsModule],
  templateUrl: './linear-regression.html',
  styleUrl: './linear-regression.css'
})
export class LinearRegression {
  hours: number | null = null;
  result = signal<number | null>(null);
  loading = signal(false);
  errorMessage = signal<string | null>(null);

  constructor(private http: HttpClient) {}

  predictGrade() {
    if (this.hours === null) {
      return;
    }
    this.loading.set(true);
    this.errorMessage.set(null);
    this.result.set(null);

    this.http.post<GradePredictionResponse>('/api/predict-grade', { hours: this.hours })
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