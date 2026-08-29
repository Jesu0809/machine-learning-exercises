import { Component, inject, signal } from '@angular/core';
import { FormBuilder, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { LinearRegressionService } from '../../services/linear-regression.service';

@Component({
  selector: 'app-linear-regression',
  imports: [FormsModule, ReactiveFormsModule],
  templateUrl: './linear-regression.html',
  styleUrl: './linear-regression.css'
})
export class LinearRegression {
  public result = signal<number | null>(null);
  public loading = signal(false);
  public errorMessage = signal<string | null>(null);

  private readonly linearRegressionService = inject(LinearRegressionService);
  private readonly formBuilder = inject(FormBuilder);

  public form = this.formBuilder.group({
    years: [null]
  });

  public predictSalary(): void {
    const years = this.form.value.years;
    console.log('hola')
    if (!years) {
      return;
    }

    this.loading.set(true);
    this.errorMessage.set(null);
    this.result.set(null);

    this.linearRegressionService.calculateSalaryPrediction(years)
      .subscribe({
        next: (response) => {
          this.result.set(response.result);
        },
        error: () => {
          this.errorMessage.set('Something went wrong. Please try again.');
        }
      });
      this.loading.set(false);
  }
}
