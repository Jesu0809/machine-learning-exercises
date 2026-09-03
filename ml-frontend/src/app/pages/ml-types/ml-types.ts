import { Component } from '@angular/core';
import { NgClass } from '@angular/common';
import { RouterLink } from '@angular/router';

interface MLTypeCard {
  name: string;
  badgeClass: string;
  definition: string;
  characteristics: string[];
  problems: string[];
  algorithms: { name: string; link?: string }[];
}

@Component({
  selector: 'app-ml-types',
  imports: [NgClass, RouterLink],
  templateUrl: './ml-types.html'
})
export class MlTypes {
  mlTypes: MLTypeCard[] = [
    {
      name: 'Supervised Learning',
      badgeClass: 'text-bg-primary',
      definition: 'The model learns from labeled data, meaning examples where the correct answer is already known, and generalizes to make predictions on new, unseen data.',
      characteristics: ['Requires labeled training data', 'Learns an input-to-output mapping', 'Performance can be measured against known correct answers'],
      problems: ['Classification (e.g. spam vs. not spam)', 'Regression (e.g. predicting a price or salary)'],
      algorithms: [
        { name: 'Linear Regression', link: '/linear-regression/concepts' },
        { name: 'Decision Trees' },
        { name: 'Support Vector Machines (SVM)' },
        { name: 'Neural Networks' }
      ]
    },
    {
      name: 'Unsupervised Learning',
      badgeClass: 'text-bg-success',
      definition: 'The model works with unlabeled data and tries to find hidden patterns, structures, or groupings on its own, without being told what the correct answer is.',
      characteristics: ['Works with unlabeled data', 'Discovers hidden structure', 'No "correct answer" to compare against'],
      problems: ['Clustering (grouping similar items)', 'Dimensionality reduction', 'Anomaly detection'],
      algorithms: [
        { name: 'K-Means' },
        { name: 'Hierarchical Clustering' },
        { name: 'PCA (Principal Component Analysis)' }
      ]
    },
    {
      name: 'Reinforcement Learning',
      badgeClass: 'text-bg-warning',
      definition: 'An agent learns to make decisions by interacting with an environment, receiving rewards or penalties based on its actions, aiming to maximize the cumulative reward over time.',
      characteristics: ['Learns through trial and error', 'Feedback comes as rewards/penalties, not labels', 'Decisions affect future states'],
      problems: ['Sequential decision-making', 'Game playing', 'Robotic control and navigation'],
      algorithms: [
        { name: 'Q-Learning' },
        { name: 'Deep Q-Networks (DQN)' },
        { name: 'Policy Gradient methods' }
      ]
    }
  ];
}
