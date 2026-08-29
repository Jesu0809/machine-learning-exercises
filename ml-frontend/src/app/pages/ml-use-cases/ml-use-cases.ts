import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MLUseCase } from '../../models/ml-use-case.model';

@Component({
  selector: 'app-ml-use-cases',
  imports: [CommonModule],
  templateUrl: './ml-use-cases.html',
  styleUrl: './ml-use-cases.css'
})
export class MlUseCases {
  useCases: MLUseCase[] = [
    {
      title: 'Image Recognition',
      description: 'Models learn to identify objects, faces, or patterns within images by training on large sets of labeled examples.',
      relatedType: 'Supervised Learning',
      examples: ['Detecting tumors in medical scans', 'Facial recognition to unlock phones', 'Quality control on factory production lines'],
      icon: 'camera'
    },
    {
      title: 'Recommendation Systems',
      description: 'Models analyze user behavior and preferences to suggest content or products the user is likely to enjoy.',
      relatedType: 'Supervised & Unsupervised Learning',
      examples: ["Netflix suggesting movies and shows", "Spotify's Discover Weekly playlist", "Amazon recommending related products"],
      icon: 'star'
    },
    {
      title: 'Fraud Detection',
      description: 'Models identify unusual patterns in data that differ from normal behavior, flagging them as potential fraud.',
      relatedType: 'Unsupervised Learning',
      examples: ['Flagging suspicious credit card transactions', 'Detecting fake insurance claims', 'Spotting identity theft attempts'],
      icon: 'shield'
    },
    {
      title: 'Autonomous Vehicles',
      description: 'An agent learns to make real-time driving decisions by interacting with its environment and being rewarded for safe, efficient behavior.',
      relatedType: 'Reinforcement Learning',
      examples: ['Self-driving cars from Tesla and Waymo', 'Autonomous drone navigation', 'Robotic delivery vehicles'],
      icon: 'car'
    }
  ];
}