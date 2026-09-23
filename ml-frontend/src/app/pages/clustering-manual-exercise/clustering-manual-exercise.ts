import { DecimalPipe } from '@angular/common';
import { Component, OnInit, computed, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { ClusteringService } from '../../services/clustering.service';
import {
  ManualCentroid,
  ManualClusteringContext,
  ManualIteration,
  ManualVarianceComparison,
} from '../../models/clustering.model';

@Component({
  selector: 'app-clustering-manual-exercise',
  imports: [RouterLink, DecimalPipe],
  templateUrl: './clustering-manual-exercise.html',
})
export class ClusteringManualExercise implements OnInit {
  private readonly service = inject(ClusteringService);

  public context = signal<ManualClusteringContext | null>(null);
  public initialCentroids = signal<ManualCentroid[]>([]);
  public iterations = signal<ManualIteration[]>([]);
  public variance = signal<ManualVarianceComparison | null>(null);

  public readonly initialPlotUrl = this.service.manualInitialPlotUrl();
  public readonly variancePlotUrl = this.service.manualVariancePlotUrl();

  public readonly iterationNumbers = [1, 2, 3];
  public activeIteration = signal(1);
  public tableLimit = 15;
  public tablePage = signal(1);

  public readonly activeIterationData = computed(() => {
    const target = this.activeIteration();
    return this.iterations().find((it) => it.iteration === target) ?? null;
  });

  public readonly pagedRecords = computed(() => {
    const data = this.activeIterationData();
    if (!data) {
      return [];
    }
    const start = (this.tablePage() - 1) * this.tableLimit;
    return data.records.slice(start, start + this.tableLimit);
  });

  public readonly totalTablePages = computed(() => {
    const data = this.activeIterationData();
    if (!data) {
      return 1;
    }
    return Math.max(1, Math.ceil(data.records.length / this.tableLimit));
  });

  public readonly rangeStart = computed(() =>
    this.pagedRecords().length === 0 ? 0 : (this.tablePage() - 1) * this.tableLimit + 1,
  );
  public readonly rangeEnd = computed(() =>
    (this.tablePage() - 1) * this.tableLimit + this.pagedRecords().length,
  );

  ngOnInit(): void {
    this.service.getManualContext().subscribe({
      next: (context) => this.context.set(context),
      error: () => {},
    });
    this.service.getManualInitialCentroids().subscribe({
      next: (centroids) => this.initialCentroids.set(centroids),
      error: () => {},
    });
    this.service.getManualVariance().subscribe({
      next: (variance) => this.variance.set(variance),
      error: () => {},
    });
    this.iterationNumbers.forEach((n) => {
      this.service.getManualIteration(n).subscribe({
        next: (iteration) =>
          this.iterations.update((list) =>
            [...list.filter((it) => it.iteration !== n), iteration].sort(
              (a, b) => a.iteration - b.iteration,
            ),
          ),
        error: () => {},
      });
    });
  }

  public selectIteration(n: number): void {
    this.activeIteration.set(n);
    this.tablePage.set(1);
  }

  public iterationPlotUrl(n: number): string {
    return this.service.manualIterationPlotUrl(n);
  }

  public previousPage(): void {
    if (this.tablePage() > 1) {
      this.tablePage.set(this.tablePage() - 1);
    }
  }

  public nextPage(): void {
    if (this.tablePage() < this.totalTablePages()) {
      this.tablePage.set(this.tablePage() + 1);
    }
  }
}
