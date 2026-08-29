import { Routes } from '@angular/router';
import { MlInfo } from './pages/ml-info/ml-info';
import { LinearRegression } from './pages/linear-regression/linear-regression';

export const routes: Routes = [
  { path: '', redirectTo: 'ml-info', pathMatch: 'full' },
  { path: 'ml-info', component: MlInfo },
  { path: 'linear-regression', component: LinearRegression },
];