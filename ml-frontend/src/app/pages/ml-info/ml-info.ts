import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { MLType } from '../../models/ml-info.model';

@Component({
  selector: 'app-ml-info',
  imports: [CommonModule, RouterLink],
  templateUrl: './ml-info.html',
  styleUrl: './ml-info.css'
})
export class MlInfo {
  mlTypes: MLType[] = [
    {
      name: 'Supervised Learning',
      description: 'The model learns from labeled data, meaning examples where the correct answer is already known. The goal is for the model to generalize and make accurate predictions on new, unseen data.',
      examples: ['Spam email detection', 'House price prediction', 'Medical diagnosis based on symptoms'],
      algorithms: [
        { name: 'Linear Regression', link: '/linear-regression' },
        { name: 'Decision Trees' },
        { name: 'Support Vector Machines (SVM)' },
        { name: 'Neural Networks' }
      ]
    },
    {
      name: 'Unsupervised Learning',
      description: 'The model works with unlabeled data and tries to find hidden patterns, structures, or groupings on its own, without being told what the correct answer is.',
      examples: ['Customer segmentation', 'Recommendation systems', 'Anomaly and fraud detection'],
      algorithms: [
        { name: 'K-Means' },
        { name: 'Hierarchical Clustering' },
        { name: 'PCA (Principal Component Analysis)' }
      ]
    },
    {
      name: 'Reinforcement Learning',
      description: 'An agent learns to make decisions by interacting with an environment, receiving rewards or penalties based on its actions, aiming to maximize the cumulative reward over time.',
      examples: ['Autonomous robotics', 'Game playing (AlphaGo)', 'Route and logistics optimization'],
      algorithms: [
        { name: 'Q-Learning' },
        { name: 'Deep Q-Networks (DQN)' },
        { name: 'Policy Gradient methods' }
      ]
    }
  ];
}