import { DecimalPipe } from '@angular/common';
import { Component, OnInit, computed, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { ReinforcementService } from '../../services/reinforcement.service';
import { GridInfo, TrainResult } from '../../models/reinforcement.model';

const QTABLE_PAGE_SIZE = 10;

@Component({
  selector: 'app-reinforcement-application',
  imports: [RouterLink, DecimalPipe],
  templateUrl: './reinforcement-application.html',
})
export class ReinforcementApplication implements OnInit {
  private readonly service = inject(ReinforcementService);

  public gridInfo = signal<GridInfo | null>(null);
  public result = signal<TrainResult | null>(null);
  public loading = signal(false);
  public errorMessage = signal<string | null>(null);
  public qTablePage = signal(0);

  public readonly rowIndices = computed(() => {
    const info = this.gridInfo();
    return info ? Array.from({ length: info.rows }, (_, i) => i) : [];
  });

  public readonly columnIndices = computed(() => {
    const info = this.gridInfo();
    return info ? Array.from({ length: info.columns }, (_, i) => i) : [];
  });

  public readonly pathSet = computed(() => {
    const response = this.result();
    if (!response) {
      return new Set<string>();
    }
    return new Set(response.path.map(([row, column]) => `${row},${column}`));
  });

  public readonly successRate = computed(() => {
    const response = this.result();
    if (!response || response.episodes === 0) {
      return 0;
    }
    return (response.successes / response.episodes) * 100;
  });

  public readonly qTablePageCount = computed(() => {
    const response = this.result();
    if (!response) {
      return 0;
    }
    return Math.ceil(response.q_table.length / QTABLE_PAGE_SIZE);
  });

  public readonly qTablePageRows = computed(() => {
    const response = this.result();
    if (!response) {
      return [];
    }
    const start = this.qTablePage() * QTABLE_PAGE_SIZE;
    return response.q_table.slice(start, start + QTABLE_PAGE_SIZE);
  });

  ngOnInit(): void {
    this.service.getGrid().subscribe({
      next: (info) => this.gridInfo.set(info),
    });
  }

  public cellLabel(row: number, column: number): string {
    const info = this.gridInfo();
    if (!info) {
      return '';
    }
    if (row === info.start[0] && column === info.start[1]) {
      return 'A';
    }
    if (row === info.goal[0] && column === info.goal[1]) {
      return 'T';
    }
    if (info.grid[row][column] === 1) {
      return '#';
    }
    if (info.grid[row][column] === 2) {
      return 'D';
    }
    return 'o';
  }

  public isWall(row: number, column: number): boolean {
    const info = this.gridInfo();
    return !!info && info.grid[row][column] === 1;
  }

  public isDanger(row: number, column: number): boolean {
    const info = this.gridInfo();
    return !!info && info.grid[row][column] === 2;
  }

  public isOnPath(row: number, column: number): boolean {
    return this.pathSet().has(`${row},${column}`);
  }

  public stateLabel(state: [number, number]): string {
    return `(${state[0]}, ${state[1]})`;
  }

  public qTablePrevPage(): void {
    this.qTablePage.update((page) => Math.max(0, page - 1));
  }

  public qTableNextPage(): void {
    this.qTablePage.update((page) =>
      Math.min(this.qTablePageCount() - 1, page + 1),
    );
  }

  public train(): void {
    this.loading.set(true);
    this.errorMessage.set(null);
    this.qTablePage.set(0);
    this.service.train().subscribe({
      next: (response) => {
        this.result.set(response);
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
}
