using System;

public class NeuralNetwork
{

    int training_iteration = 0;

    private int numInput; // Number of input nodes
    private int numHidden; // Number of hidden nodes
    private int numOutput; // Number of output nodes

    private double[] inputs;
    private double[,] input_to_hidden_weights; // Input-to-hidden weights
    private double[,] hoWeights; // Hidden-to-output weights
    public double[] errors; // Errors between actual, and the predicted value


    private Random random;

    // Constructor
    public NeuralNetwork(int numInput, int numHidden, int numOutput)
    {
        this.numInput = numInput;
        this.numHidden = numHidden;
        this.numOutput = numOutput;

        inputs = new double[numInput];
        input_to_hidden_weights = new double[numInput, numHidden];
        hoWeights = new double[numHidden, numOutput];
        errors = new double[numOutput];


        random = new Random();

        // Initialize weights and biases with random values
        InitializeWeights();
    }

    // Initialize weights and biases with random values
    private void InitializeWeights()
    {
        for (int i = 0; i < numInput; i++)
        {
            for (int j = 0; j < numHidden; j++)
            {
                input_to_hidden_weights[i, j] = random.NextDouble() - 0.5; // Random value between -0.5 and 0.5
            }
        }

        for (int i = 0; i < numHidden; i++)
        {
            for (int j = 0; j < numOutput; j++)
            {
                hoWeights[i, j] = random.NextDouble() - 0.5;
            }
        }

    }

    // Forward propagation
    public double[] Forward(double[] input)
    {
        // Copy input values to the input nodes
        Array.Copy(input, inputs, numInput);

        // Compute hidden layer activations
        double[] hiddenOutputs = new double[numHidden];
        for (int j = 0; j < numHidden; j++)
        {
            double sum = 0.0;
            for (int i = 0; i < numInput; i++)
            {
                sum += inputs[i] * input_to_hidden_weights[i, j];
            }
            hiddenOutputs[j] = Sigmoid(sum);
        }

        // Compute output layer activations
        double[] outputs = new double[numOutput];
        for (int j = 0; j < numOutput; j++)
        {
            double sum = 0.0;
            for (int i = 0; i < numHidden; i++)
            {
                sum += hiddenOutputs[i] * hoWeights[i, j];
            }
            outputs[j] = Sigmoid(sum);
        }

        return outputs;
    }

    // Sigmoid activation function
    private double Sigmoid(double x)
    {
        return 1.0 / (1.0 + Math.Exp(-x));
    }

    // Train the model (very basic training method)
    public void Train(double[] input, double[] target)
    {
        training_iteration++;
        // Perform forward pass to get outputs
        double[] outputs = Forward(input);

        // Adjust weights and biases randomly
        for (int i = 0; i < numInput; i++)
        {
            for (int j = 0; j < numHidden; j++)
            {
                input_to_hidden_weights[i, j] += random.NextDouble(); // Random adjustment
            }
        }

        for (int i = 0; i < numHidden; i++)
        {
            for (int j = 0; j < numOutput; j++)
            {
                hoWeights[i, j] += random.NextDouble() - 0.5; // Random adjustment
            }
        }
    }


    private void UpdateWeights(double[] newWeights)
    {
        int k = 0;
        for (int i = 0; i < numInput; i++)
        {
            for (int j = 0; j < numHidden; j++)
            {
                input_to_hidden_weights[i, j] += newWeights[k++];
            }
        }

        for (int i = 0; i < numHidden; i++)
        {
            for (int j = 0; j < numOutput; j++)
            {
                hoWeights[i, j] += newWeights[k++];
            }
        }
    }


    // Perturb the weights slightly
    private double[] PerturbWeights(double magnitude)
    {
        double[] perturbedWeights = new double[numInput * numHidden + numHidden * numOutput];
        for (int i = 0; i < perturbedWeights.Length; i++)
        {
            perturbedWeights[i] = random.NextDouble() * magnitude - magnitude / 2.0; // Random adjustment within the specified magnitude
        }
        return perturbedWeights;
    }


    // Train the model using hill climbing
    public void HillClimbTrain(double[] input, double[] target, int maxIterations)
    {

        double[] bestWeights = new double[numInput * numHidden + numHidden * numOutput]; // Store the best weights found
        double bestError = double.MaxValue; // Initialize the best error to a large value

        for (int iteration = 0; iteration < maxIterations; iteration++)
        {
            // Perturb the weights slightly
            double[] perturbedWeights = PerturbWeights(0.1); // Adjust the perturbation magnitude as needed

            // Update the network with perturbed weights
            UpdateWeights(perturbedWeights);

            // Perform forward pass with perturbed weights
            double[] output = Forward(input);

            // Calculate mean squared error with perturbed weights
            double error = MeanSquaredError(target, output);

            // If the error with perturbed weights is better than the best error, update the best error and weights
            if (error < bestError)
            {
                bestError = error;
                Array.Copy(perturbedWeights, bestWeights, perturbedWeights.Length);
                Console.WriteLine($"[ITERATION: {training_iteration++}] Output {output[0]}");
                Console.WriteLine("Error: " + error);
            }
        }

        // Update the network with the best weights found
        UpdateWeights(bestWeights);
    }

    // Compute mean squared error
    private double MeanSquaredError(double[] target, double[] output)
    {
        double sumSquaredError = 0.0;
        for (int i = 0; i < target.Length; i++)
        {
            double error = target[i] - output[i];
            sumSquaredError += error * error;
        }
        return sumSquaredError / target.Length;
    }

    public static void Main(string[] args)
    {
        // Define neural network parameters
        int numInput = 4;
        int numHidden = 4;
        int numOutput = 1;


        // Create a neural network instance
        NeuralNetwork neuralNetwork = new NeuralNetwork(numInput, numHidden, numOutput);

        // Input values for training
        double[] input = { 0.5, 0.3, 0.2, 0.7 };
        double[] target = { 0.8 }; // Target output value

        // Train the model
        neuralNetwork.Train(input, target);

        // Perform forward pass with the same input to see the updated output
        double[] output = neuralNetwork.Forward(input);


        // Display the updated output
        Console.WriteLine("Updated Output: ");

        for (int i = 0; i < numOutput; i++)
        {
            neuralNetwork.errors[i] = Math.Abs(output[i] - target[i]);
            Console.WriteLine($"Output {output[i]}");
            Console.WriteLine("Error: " + Math.Abs(output[i] - target[i]));
        }


        // Hill Climb Training
        Console.WriteLine();
        neuralNetwork.HillClimbTrain(input, target, 1000000);

        /* while (neuralNetwork.errors[0] > 0.01)
        {
            neuralNetwork.Train(input, target);
            for (int i = 0; i < numOutput; i++)
            {
                neuralNetwork.errors[i] = Math.Abs(output[i] - target[i]);
                // Weight Randomization
                Console.WriteLine($"[ITERATION: {neuralNetwork.training_iteration}] Output {output[i]}");
                Console.WriteLine("Error: " + (output[i] - target[i]));
            }
            output = neuralNetwork.Forward(input);
        } */
        Console.ReadLine();
    }
}
