export interface Algorithm {
  name: string;
  link?: string;
}

export interface MLType {
  name: string;
  description: string;
  examples: string[];
  algorithms: Algorithm[];
}