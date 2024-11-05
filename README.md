# BlokusDuo
An exploration into the game of [Blokus](https://en.wikipedia.org/wiki/Blokus) through various algorithms.
### By Jake Frischmann, Etash Jhanji, Alden Bressler, Delia Brown, Micheal Huang, and Sebastian Liu


[PGSS Project Paper](https://tesdnet-my.sharepoint.com/:w:/g/personal/25frischmannj_tesdk12_net/Eaq9sagThWhFvesd_CqsRSwBd00tdYPEoN6t86uTtX1hGA?e=fx7OIc)

## A Quick Abstract

This repository explores the application of various artificial intelligence algorithms to a two-player, abstract strategy board game Blokus Duo, evaluating the performance of models in different simulated environments. We implemented and tested several AI approaches, including Minimax (v3), Proximal Policy Optimization (PPO, v1), and Monte Carlo Tree Search (MCTS) with and without two convolutional neural networks (CNN) as evaluation and policy functions. Our primary objective was to compare the effectiveness of these algorithms in both human and non-human gameplay and identify trends in performance, particularly against human players. 

We conducted over 2.5 million simulations across different model configurations, with random play serving as a baseline for performance evaluation. We found that Minimax, despite being a relatively simple algorithm, performed competitively in random agent simulations and showed a high win rate. In non-random matchups, Minimax and MCTS demonstrated superior performance, particularly in human play scenarios. MCTS, when augmented with CNNs, achieved the highest win rates overall, benefiting from the added complexity of the neural networks, and their ability to reduce the width and depth of search trees, which enabled more informed decision-making during play. The results suggest that MCTS, both with and without CNNs, can outperform experienced human players and other AI models, highlighting its effectiveness in strategic games like Blokus Duo. 

The PPO model, however, exhibited poor performance in matchups against more complex algorithms, likely due to insufficient training data and suboptimal hyperparameter tuning. Although it demonstrated strong results against random agents, its weaknesses were evident when facing experienced human players and more sophisticated AI. The deterministic nature of both PPO and Minimax prevented meaningful results when they were pitted against each other, leading to omitted data in this area. 

Due to time constraints, certain comparisons, such as those involving PPO versus MCTS with CNN, could not be completed. However, based on similar trends observed in other matchups, we hypothesize that results would mirror those seen with MCTS alone, given the similar performance patterns of both models in comparable scenarios. 

The research concludes that MCTS, particularly when combined with CNNs, is the most effective algorithm tested for this strategic game. Future work will focus on refining code to reduce simulation runtime, experimenting with more sophisticated systems, and testing these advanced AI models against a broader pool of human players to validate their real-world applicability. 

All code developed for this project is available on GitHub for further exploration and development. 

