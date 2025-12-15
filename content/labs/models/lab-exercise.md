# LabExercise Model Definition

## Overview

This document defines the structure and validation rules for lab exercises in the AI textbook.

## Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | string | Yes | Unique identifier for the lab exercise |
| title | string | Yes | Title of the exercise |
| description | string | Yes | Brief description of what the exercise covers |
| prerequisites | array of strings | No | Array of module IDs or skills required |
| estimatedDuration | number | Yes | Time estimate in minutes (positive value) |
| notebookUrl | string | Yes | URL to the cloud-based notebook environment |
| objectives | array of strings | Yes | Array of learning objectives (non-empty) |
| steps | array of strings | Yes | Ordered array of instructions for the exercise (non-empty) |
| datasets | array of strings | No | Array of dataset names or URLs used in the exercise |
| hardwareRequirements | string | No | Reference to hardware profile |
| difficultyLevel | string | No | Level of difficulty (beginner, intermediate, advanced) |
| tags | array of strings | No | Array of tags for categorizing the exercise |
| createdAt | datetime | No | Timestamp of creation |
| updatedAt | datetime | No | Timestamp of last update |

## Relationships

- Connects to one or more Modules/Chapters
- Associated with one HardwareProfile
- Contains one or more CodeSnippets

## Validation Rules

- title and description are required
- estimatedDuration must be positive
- notebookUrl must be a valid cloud notebook URL
- objectives array must not be empty
- steps array must not be empty
- hardwareRequirements must refer to an existing hardware profile

## Example

```yaml
id: "neural-network-basics-lab"
title: "Neural Network Basics Lab"
description: "In this lab, you will build a simple neural network from scratch using TensorFlow to classify handwritten digits."
prerequisites: ["module-1", "linear-algebra"]
estimatedDuration: 45
notebookUrl: "https://colab.research.google.com/example"
objectives: 
  - "Implement a basic neural network from scratch"
  - "Understand forward and backward propagation"
  - "Train a model on MNIST dataset"
steps:
  - "Import required libraries"
  - "Load and preprocess the data"
  - "Define the neural network architecture"
  - "Train the model"
  - "Evaluate the model's performance"
datasets: ["MNIST", "Fashion-MNIST"]
hardwareRequirements: "gpu-recommended"
difficultyLevel: "intermediate"
tags: ["neural-networks", "tensorflow"]
createdAt: "2025-12-15T10:00:00Z"
updatedAt: "2025-12-15T10:00:00Z"
```