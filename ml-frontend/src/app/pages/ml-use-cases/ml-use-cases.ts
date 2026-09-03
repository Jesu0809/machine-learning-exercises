import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-ml-use-cases',
  imports: [RouterLink],
  templateUrl: './ml-use-cases.html'
})
export class MlUseCases {
  useCases = [
    { title: 'Use Case 1: Image Recognition for Medical Diagnosis', type: 'Supervised Learning', link: '/use-cases/1' },
    { title: 'Use Case 2: Personalized Recommendation Systems', type: 'Supervised & Unsupervised Learning', link: '/use-cases/2' },
    { title: 'Use Case 3: Fraud Detection in Financial Transactions', type: 'Unsupervised Learning', link: '/use-cases/3' },
    { title: 'Use Case 4: Autonomous Vehicle Navigation', type: 'Reinforcement Learning', link: '/use-cases/4' }
  ];
}
