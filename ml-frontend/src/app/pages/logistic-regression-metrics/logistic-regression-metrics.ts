import { DecimalPipe, PercentPipe } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { LogisticRegressionService } from '../../services/logistic-regression.service';
import { ClassMetrics } from '../../models/classification.model';

@Component({
  selector: 'app-logistic-regression-metrics',
  imports: [RouterLink, DecimalPipe, PercentPipe],
  templateUrl: './logistic-regression-metrics.html',
})
export class LogisticRegressionMetrics implements OnInit {
  private readonly service = inject(LogisticRegressionService);

  public metrics = signal<ClassMetrics | null>(null);
  public readonly confusionPlotUrl = this.service.confusionPlotUrl();

  ngOnInit(): void {
    this.service.getMetrics().subscribe({
      next: (value) => this.metrics.set(value),
      error: () => {},
    });
  }
}
