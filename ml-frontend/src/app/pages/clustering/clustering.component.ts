import { DecimalPipe, PercentPipe } from '@angular/common';
import { Component, OnInit, computed, inject, signal } from '@angular/core';
import { FormBuilder, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { ClusteringService } from '../../services/clustering.service';
import {
  ClusterInfo,
  ClusterInput,
  ClusterMetrics,
  ClusterRecord,
  ClusterResult,
} from '../../models/clustering.model';

@Component({
  selector: 'app-clustering',
  imports: [FormsModule, ReactiveFormsModule, RouterLink, DecimalPipe, PercentPipe],
  templateUrl: './clustering.component.html',
})
export class ClusteringComponent implements OnInit {
  private readonly service = inject(ClusteringService);
  private readonly formBuilder = inject(FormBuilder);

  public modelInfo = signal<ClusterInfo | null>(null);
  public metrics = signal<ClusterMetrics | null>(null);
  public result = signal<ClusterResult | null>(null);
  public loading = signal(false);
  public errorMessage = signal<string | null>(null);
  public plotUrl = signal<string>(this.service.scatterPlotUrl());
  public readonly elbowPlotUrl = this.service.elbowPlotUrl();

  public form = this.formBuilder.group({
    annual_income: [null as number | null],
    debt_to_income_ratio: [null as number | null],
    credit_history_length: [null as number | null],
    open_credit_lines: [null as number | null],
  });

  public readonly fields: { key: keyof ClusterInput; label: string; unit: string; placeholder: string }[] = [
    { key: 'annual_income', label: 'Annual income', unit: 'USD', placeholder: 'e.g. 90000' },
    { key: 'debt_to_income_ratio', label: 'Debt-to-income ratio', unit: '%', placeholder: 'e.g. 18' },
    { key: 'credit_history_length', label: 'Credit history length', unit: 'years', placeholder: 'e.g. 12' },
    { key: 'open_credit_lines', label: 'Open credit lines', unit: 'count', placeholder: 'e.g. 3' },
  ];

  public readonly clusterOrder = computed(() => {
    const info = this.modelInfo();
    if (!info) {
      return [];
    }
    return Object.keys(info.clusterNames)
      .map(Number)
      .sort((a, b) => a - b);
  });

  limitOptions = [10, 20, 50, 100];
  limit = 20;
  page = signal(1);
  totalPages = signal(1);
  totalRecords = signal(0);
  records = signal<ClusterRecord[]>([]);
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
    this.service.getMetrics().subscribe({
      next: (metrics) => this.metrics.set(metrics),
      error: () => {},
    });
    this.fetchData();
  }

  public control(key: keyof ClusterInput) {
    return this.form.get(key);
  }

  public assignCluster(): void {
    this.form.markAllAsTouched();
    if (this.form.invalid) {
      return;
    }
    const values: ClusterInput = {
      annual_income: Number(this.form.value.annual_income),
      debt_to_income_ratio: Number(this.form.value.debt_to_income_ratio),
      credit_history_length: Number(this.form.value.credit_history_length),
      open_credit_lines: Number(this.form.value.open_credit_lines),
    };
    this.loading.set(true);
    this.errorMessage.set(null);

    this.service.predict(values).subscribe({
      next: (response) => {
        this.result.set(response);
        this.plotUrl.set(this.service.scatterPlotUrl(values));
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
