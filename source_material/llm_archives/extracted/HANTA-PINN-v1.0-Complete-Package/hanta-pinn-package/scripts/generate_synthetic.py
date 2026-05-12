#!/usr/bin/env python
"""Generate synthetic SEIR trajectories for pretraining."""
import argparse
import pickle
from src.physics.seir_rhs import generate_synthetic_dataset


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=int, default=10000)
    parser.add_argument('--output', default='data/synthetic/trajectories.pkl')
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--test_mode', action='store_true')
    args = parser.parse_args()

    if args.test_mode:
        print("Test mode: generating 100 trajectories...")
        args.n = 100

    trajectories = generate_synthetic_dataset(n=args.n, seed=args.seed)

    with open(args.output, 'wb') as f:
        pickle.dump(trajectories, f)

    print(f"Generated {args.n} trajectories. Saved to {args.output}")


if __name__ == '__main__':
    main()
