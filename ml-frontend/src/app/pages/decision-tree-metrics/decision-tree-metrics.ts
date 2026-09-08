import { DecimalPipe, PercentPipe } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { DecisionTreeService } from '../../services/decision-tree.service';
import { LogisticRegressionService } from '../../services/logistic-regression.service';
import { ClassMetrics } from '../../models/classification.model';

@Component({
  selector: 'app-decision-tree-metrics',
  imports: [RouterLink, DecimalPipe, PercentPipe],
  templateUrl: './decision-tree-metrics.html',
})
export class DecisionTreeMetrics implements OnInit {
  private readonly treeService = inject(DecisionTreeService);
  private readonly logRegService = inject(LogisticRegressionService);

  public metrics = signal<ClassMetrics | null>(null);
  public logRegMetrics = signal<ClassMetrics | null>(null);
  public readonly confusionPlotUrl = this.treeService.confusionPlotUrl();

  ngOnInit(): void {
    this.treeService.getMetrics().subscribe({
      next: (value) => this.metrics.set(value),
      error: () => {},
    });
    this.logRegService.getMetrics().subscribe({
      next: (value) => this.logRegMetrics.set(value),
      error: () => {},
    });
  }
}
