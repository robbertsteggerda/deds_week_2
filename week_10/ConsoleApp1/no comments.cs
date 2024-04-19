using System;

public class NeuralNetwork
{

    int training_iteration = 0;

    private int numInput;
    private int numHidden;
    private int numOutput;

    private double[] inputs;
    private double[,] input_to_hidden_weights;
    private double[,] hidden_to_output_weights;
    public double[] errors;


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

        
        InitializeWeights();
    }

    
    private void InitializeWeights()
    {
        for (int i = 0; i < numInput; i++)
        {
            for (int j = 0; j < numHidden; j++)
            {
                input_to_hidden_weights[i, j] = random.NextDouble() - 0.5;
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

    
    public double[] Forward(double[] input)
    {
    
        Array.Copy(input, inputs, numInput);

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

    private double Sigmoid(double x)
    {
        return 1.0 / (1.0 + Math.Exp(-x));
    }

    public void Train(double[] input, double[] target)
    {
        training_iteration++;
        double[] outputs = Forward(input);

        for (int i = 0; i < numInput; i++)
        {
            for (int j = 0; j < numHidden; j++)
            {
                input_to_hidden_weights[i, j] += random.NextDouble();
            }
        }

        for (int i = 0; i < numHidden; i++)
        {
            for (int j = 0; j < numOutput; j++)
            {
                hidden_to_output_weights[i, j] += random.NextDouble() - 0.5;
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


    
    private double[] PerturbWeights(double magnitude)
    {
        double[] perturbedWeights = new double[numInput * numHidden + numHidden * numOutput];
        for (int i = 0; i < perturbedWeights.Length; i++)
        {
            perturbedWeights[i] = random.NextDouble() * magnitude - magnitude / 2.0;
        }
        return perturbedWeights;
    }



    public void HillClimbTrain(double[] input, double[] target, int maxIterations)
    {

        double[] bestWeights = new double[numInput * numHidden + numHidden * numOutput]; 
        double bestError = double.MaxValue;

        for (int iteration = 0; iteration < maxIterations; iteration++)
        {
            
            double[] perturbedWeights = PerturbWeights(0.1); 

            
            UpdateWeights(perturbedWeights);

            
            double[] output = Forward(input);

            
            double error = MeanSquaredError(target, output);

            
            if (error < bestError)
            {
                bestError = error;
                Array.Copy(perturbedWeights, bestWeights, perturbedWeights.Length);
                Console.WriteLine($"[ITERATION: {training_iteration++}] Output {output[0]}");
                Console.WriteLine("Error: " + error);
            }
        }

        
        UpdateWeights(bestWeights);
    }

    
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
    
        int numInput = 4;
        int numHidden = 4;
        int numOutput = 1;


        NeuralNetwork neuralNetwork = new NeuralNetwork(numInput, numHidden, numOutput);

        double[] input = { 0.5, 0.3, 0.2, 0.7 };
        double[] target = { 0.8 };

        neuralNetwork.Train(input, target);

        double[] output = neuralNetwork.Forward(input);

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
