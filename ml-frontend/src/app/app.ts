import { Component, signal } from '@angular/core';
import { MlInfo } from './ml-info/ml-info';

@Component({
  imports: [MlInfo],
  selector: 'app-root',
  styleUrl: './app.css',
  templateUrl: './app.html',
})
export class App {
  protected readonly title = signal('ml-frontend');
}
