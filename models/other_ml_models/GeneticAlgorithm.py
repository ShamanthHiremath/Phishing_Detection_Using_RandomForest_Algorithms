# Import necessary libraries
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score
import joblib

# Define the dataset and preprocessing
dataset = pd.read_csv("datasets/phishyFeatures.csv")
dataset = dataset.drop('id', axis=1)

# Split data into features (x) and target (y)
x = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values.ravel()

# Splitting the dataset into training set and test set
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=0)

# Define a function to evaluate fitness (accuracy in this case)
def evaluate_fitness(params):
    n_estimators, max_features, criterion = params
    model = RandomForestClassifier(n_estimators=n_estimators, max_features=max_features, criterion=criterion, random_state=0)
    cv_score = cross_val_score(model, x_train, y_train, cv=3, scoring='accuracy').mean()
    return cv_score

# Genetic Algorithm parameters
POP_SIZE = 10
NUM_GENERATIONS = 5
MUTATION_RATE = 0.1
CROSSOVER_RATE = 0.8

# Define the initial population randomly
def initialize_population(pop_size):
    population = []
    for _ in range(pop_size):
        n_estimators = np.random.choice([100, 700])
        max_features = np.random.choice(['sqrt', 'log2'])
        criterion = np.random.choice(['gini', 'entropy'])
        population.append((n_estimators, max_features, criterion))
    return population

# Genetic Algorithm main loop
population = initialize_population(POP_SIZE)
for generation in range(NUM_GENERATIONS):
    # Evaluate fitness for each individual in the population
    fitness_scores = [evaluate_fitness(params) for params in population]

    # Select parents based on fitness scores (tournament selection)
    selected_indices = np.random.choice(range(POP_SIZE), size=POP_SIZE, replace=True, p=fitness_scores / np.sum(fitness_scores))

    # Create offspring through crossover
    offspring = []
    for i in range(0, POP_SIZE, 2):
        parent1 = population[selected_indices[i]]
        parent2 = population[selected_indices[i+1]]
        if np.random.rand() < CROSSOVER_RATE:
            crossover_point = np.random.randint(1, 3)
            child1 = parent1[:crossover_point] + parent2[crossover_point:]
            child2 = parent2[:crossover_point] + parent1[crossover_point:]
            offspring.extend([child1, child2])
        else:
            offspring.extend([parent1, parent2])

    # Apply mutation to offspring
    for i in range(len(offspring)):
        if np.random.rand() < MUTATION_RATE:
            mutation_point = np.random.randint(0, 3)
            if mutation_point == 0:
                offspring[i] = (np.random.choice([100, 700]), offspring[i][1], offspring[i][2])
            elif mutation_point == 1:
                offspring[i] = (offspring[i][0], np.random.choice(['sqrt', 'log2']), offspring[i][2])
            else:
                offspring[i] = (offspring[i][0], offspring[i][1], np.random.choice(['gini', 'entropy']))

    # Replace the population with the offspring
    population = offspring

# Select the best individual (parameters)
best_params = max(population, key=lambda params: evaluate_fitness(params))

# Train the final model with the best parameters
final_model = RandomForestClassifier(n_estimators=best_params[0], max_features=best_params[1], criterion=best_params[2], random_state=0)
final_model.fit(x_train, y_train)

# Evaluate on test set
y_pred = final_model.predict(x_test)
test_accuracy = accuracy_score(y_test, y_pred)
print(f"Test Accuracy: {test_accuracy}")

# Save the final model
joblib.dump(final_model, 'trained_models/genetic_algo_randomForest_final.pkl', protocol=4)
