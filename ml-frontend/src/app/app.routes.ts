import { Routes } from '@angular/router';
import { Home } from './pages/home/home';
import { MlInfo } from './pages/ml-info/ml-info';
import { MlTypes } from './pages/ml-types/ml-types';
import { MlUseCases } from './pages/ml-use-cases/ml-use-cases';
import { UseCase1 } from './pages/use-case-1/use-case-1';
import { UseCase2 } from './pages/use-case-2/use-case-2';
import { UseCase3 } from './pages/use-case-3/use-case-3';
import { UseCase4 } from './pages/use-case-4/use-case-4';
import { LinearRegressionConcepts } from './pages/linear-regression-concepts/linear-regression-concepts';
import { LinearRegressionApplication } from './pages/linear-regression-application/linear-regression-application';

export const routes: Routes = [
  { path: '', component: Home, pathMatch: 'full' },
  { path: 'ml-info', component: MlInfo },
  { path: 'ml-types', component: MlTypes },
  { path: 'ml-use-cases', component: MlUseCases },
  { path: 'use-cases/1', component: UseCase1 },
  { path: 'use-cases/2', component: UseCase2 },
  { path: 'use-cases/3', component: UseCase3 },
  { path: 'use-cases/4', component: UseCase4 },
  { path: 'linear-regression/concepts', component: LinearRegressionConcepts },
  { path: 'linear-regression/application', component: LinearRegressionApplication },
];
