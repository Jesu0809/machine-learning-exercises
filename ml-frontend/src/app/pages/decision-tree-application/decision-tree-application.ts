import { DecimalPipe, PercentPipe } from '@angular/common';
import { Component, OnInit, computed, inject, signal } from '@angular/core';
import { FormBuilder, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { DecisionTreeService } from '../../services/decision-tree.service';
import { TreeInfo, TreeInput, TreeRecord, TreeResult } from '../../models/classification.model';

@Component({
  selector: 'app-decision-tree-application',
  imports: [FormsModule, ReactiveFormsModule, RouterLink, DecimalPipe, PercentPipe],
  templateUrl: './decision-tree-application.html',
})
export class DecisionTreeApplication implements OnInit {
  private readonly service = inject(DecisionTreeService);
  private readonly formBuilder = inject(FormBuilder);

  public modelInfo = signal<TreeInfo | null>(null);
  public importances = signal<{ name: string; value: number }[]>([]);
  public result = signal<TreeResult | null>(null);
  public loading = signal(false);
  public errorMessage = signal<string | null>(null);
  public plotUrl = signal<string>(this.service.scatterPlotUrl());
  public readonly importancePlotUrl = this.service.importancePlotUrl();

  public form = this.formBuilder.group({
    annual_income: [null as number | null, [Validators.required, Validators.min(0)]],
    debt_to_income_ratio: [
      null as number | null,
      [Validators.required, Validators.min(0), Validators.max(100)],
    ],
    credit_history_length: [null as number | null, [Validators.required, Validators.min(0), Validators.max(100)]],
    open_credit_lines: [null as number | null, [Validators.required, Validators.min(0)]],
  });

  public readonly fields: { key: keyof TreeInput; label: string; unit: string; placeholder: string; max?: number }[] = [
    { key: 'annual_income', label: 'Annual income', unit: 'USD', placeholder: 'e.g. 90000' },
    { key: 'debt_to_income_ratio', label: 'Debt-to-income ratio', unit: '%', placeholder: 'e.g. 18', max: 100 },
    { key: 'credit_history_length', label: 'Credit history length', unit: 'years', placeholder: 'e.g. 12', max: 100 },
    { key: 'open_credit_lines', label: 'Open credit lines', unit: 'count', placeholder: 'e.g. 3' },
  ];

  limitOptions = [10, 20, 50, 100];
  limit = 20;
  page = signal(1);
  totalPages = signal(1);
  totalRecords = signal(0);
  records = signal<TreeRecord[]>([]);
  tableLoading = signal(false);

  public readonly rangeStart = computed(() =>
    this.totalRecords() === 0 ? 0 : (this.page() - 1) * this.limit + 1,
  );
  public readonly rangeEnd = computed(() =>
    Math.min(this.page() * this.limit, this.totalRecords()),
  );

  ngOnInit(): void {
    this.service.getModelInfo().subscribe({
      next: (info) => {
        this.modelInfo.set(info);
        this.importances.set(
          Object.entries(info.featureImportances)
            .map(([name, value]) => ({ name, value }))
            .sort((a, b) => b.value - a.value),
        );
      },
      error: () => {},
    });
    this.fetchData();
  }

  public control(key: keyof TreeInput) {
    return this.form.get(key);
  }

  public classify(): void {
    this.form.markAllAsTouched();
    if (this.form.invalid) {
      return;
    }
    const values: TreeInput = {
      annual_income: Number(this.form.value.annual_income),
      debt_to_income_ratio: Number(this.form.value.debt_to_income_ratio),
      credit_history_length: Number(this.form.value.credit_history_length),
      open_credit_lines: Number(this.form.value.open_credit_lines),
    };
    this.loading.set(true);
    this.errorMessage.set(null);

    this.service.classify(values).subscribe({
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
