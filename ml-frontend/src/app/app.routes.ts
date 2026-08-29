import { Routes } from '@angular/router';
import { MlInfo } from './pages/ml-info/ml-info';
import { MlUseCases } from './pages/ml-use-cases/ml-use-cases';
import { LinearRegression } from './pages/linear-regression/linear-regression';

export const routes: Routes = [
  { path: '', redirectTo: 'ml-info', pathMatch: 'full' },
  { path: 'ml-info', component: MlInfo },
  { path: 'ml-use-cases', component: MlUseCases },
  { path: 'linear-regression', component: LinearRegression },
];