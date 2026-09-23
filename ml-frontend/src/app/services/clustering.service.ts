import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { DatasetPage } from '../models/classification.model';
import {
  ClusterInfo,
  ClusterInput,
  ClusterMetrics,
  ClusterRecord,
  ClusterResult,
  ManualClusteringContext,
  ManualCentroid,
  ManualIteration,
  ManualVarianceComparison,
} from '../models/clustering.model';

@Injectable({ providedIn: 'root' })
export class ClusteringService {
  private readonly http = inject(HttpClient);

  predict(values: ClusterInput): Observable<ClusterResult> {
    return this.http.post<ClusterResult>('/api/clustering/predict', values);
  }

  getModelInfo(): Observable<ClusterInfo> {
    return this.http.get<ClusterInfo>('/api/clustering/model-info');
  }

  getMetrics(): Observable<ClusterMetrics> {
    return this.http.get<ClusterMetrics>('/api/clustering/metrics');
  }

  getDataset(page: number, limit: number): Observable<DatasetPage<ClusterRecord>> {
    return this.http.get<DatasetPage<ClusterRecord>>(
      `/api/clustering/dataset?page=${page}&limit=${limit}`,
    );
  }

  scatterPlotUrl(values?: ClusterInput | null): string {
    if (!values) {
      return '/api/clustering/scatter-plot';
    }
    const query = new URLSearchParams(
      Object.entries(values).map(([key, value]) => [key, String(value)]),
    ).toString();
    return `/api/clustering/scatter-plot?${query}`;
  }

  elbowPlotUrl(): string {
    return '/api/clustering/elbow-plot';
  }

  getManualContext(): Observable<ManualClusteringContext> {
    return this.http.get<ManualClusteringContext>('/api/manual-clustering/context');
  }

  getManualInitialCentroids(): Observable<ManualCentroid[]> {
    return this.http.get<ManualCentroid[]>('/api/manual-clustering/initial-centroids');
  }

  getManualIteration(n: number): Observable<ManualIteration> {
    return this.http.get<ManualIteration>(`/api/manual-clustering/iteration/${n}`);
  }

  getManualVariance(): Observable<ManualVarianceComparison> {
    return this.http.get<ManualVarianceComparison>('/api/manual-clustering/variance');
  }

  manualInitialPlotUrl(): string {
    return '/api/manual-clustering/initial-plot';
  }

  manualIterationPlotUrl(n: number): string {
    return `/api/manual-clustering/iteration-plot/${n}`;
  }

  manualVariancePlotUrl(): string {
    return '/api/manual-clustering/variance-plot';
  }
}
