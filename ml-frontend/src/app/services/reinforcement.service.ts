import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { GridInfo, TrainResult } from '../models/reinforcement.model';

@Injectable({ providedIn: 'root' })
export class ReinforcementService {
  private readonly http = inject(HttpClient);

  getGrid(): Observable<GridInfo> {
    return this.http.get<GridInfo>('/api/reinforcement/grid');
  }

  train(): Observable<TrainResult> {
    return this.http.post<TrainResult>('/api/reinforcement/train', {});
  }
}
