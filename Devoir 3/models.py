import nn
from backend import PerceptronDataset, RegressionDataset, DigitClassificationDataset


class PerceptronModel(object):
    def __init__(self, dimensions: int) -> None:
        """
        Initialize a new Perceptron instance.

        A perceptron classifies data points as either belonging to a particular
        class (+1) or not (-1). `dimensions` is the dimensionality of the data.
        For example, dimensions=2 would mean that the perceptron must classify
        2D points.
        """
        self.w = nn.Parameter(1, dimensions)

    def get_weights(self) -> nn.Parameter:
        """
        Return a Parameter instance with the current weights of the perceptron.
        """
        return self.w

    def run(self, x: nn.Constant) -> nn.Node:
        """
        Calculates the score assigned by the perceptron to a data point x.

        Inputs:
            x: a node with shape (1 x dimensions)
        Returns: a node containing a single number (the score)
        """
        "*** TODO: COMPLETE HERE FOR QUESTION 1 ***"
        return nn.DotProduct(x, self.w)

    def get_prediction(self, x: nn.Constant) -> int:
        """
        Calculates the predicted class for a single data point `x`.

        Returns: 1 or -1
        """
        "*** TODO: COMPLETE HERE FOR QUESTION 1 ***"
        ps = nn.as_scalar(self.run(x))
        if ps >= 0: 
            return 1
        else : 
            return -1


    def train(self, dataset: PerceptronDataset) -> None:
        """
        Train the perceptron until convergence.
        """
        "*** TODO: COMPLETE HERE FOR QUESTION 1 ***"
        done = False
        while not done: 
            batch_size = 1
            all_predicted = True
            for x, y in dataset.iterate_once(batch_size):
                y_hat = self.get_prediction(x)
                y_s = nn.as_scalar(y)
                all_predicted = all_predicted and (y_hat == y_s)
                if y_hat != y_s: 
                    self.w.update(x, multiplier=y_s)
            done = all_predicted
                    




class RegressionModel(object):
    """
    A neural network model for approximating a function that maps from real
    numbers to real numbers. The network should be sufficiently large to be able
    to approximate sin(x) on the interval [-2pi, 2pi] to reasonable precision.
    """

    def __init__(self) -> None:
        # Initialize your model parameters here
        "*** TODO: COMPLETE HERE FOR QUESTION 2 ***"
        self.nb_neurons = 128
        self.w1 = nn.Parameter(1, self.nb_neurons)
        self.b1 = nn.Parameter(1, self.nb_neurons)
        self.w2 = nn.Parameter(self.nb_neurons, self.nb_neurons)
        self.b2 = nn.Parameter(1, self.nb_neurons)
        self.w3 = nn.Parameter(self.nb_neurons, self.nb_neurons)
        self.b3 = nn.Parameter(1, self.nb_neurons)
        self.w4 = nn.Parameter(self.nb_neurons, 1)
        self.b4 = nn.Parameter(1, 1)

    def run(self, x: nn.Constant) -> nn.Node:
        """
        Runs the model for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
        Returns:
            A node with shape (batch_size x 1) containing predicted y-values
        """
        "*** TODO: COMPLETE HERE FOR QUESTION 2 ***"
        ## 1ere couche
        z1 = nn.Linear(x,self.w1)
        z1 = nn.AddBias(z1, self.b1)
        a1 = nn.ReLU(z1)
        ## 2eme couche
        z2 = nn.Linear(a1,self.w2)
        z2 = nn.AddBias(z2, self.b2)
        a2 = nn.ReLU(z2)
        ## 3eme couche
        z3 = nn.Linear(a2,self.w3)
        z3 = nn.AddBias(z3, self.b3)
        a3 = nn.ReLU(z3)
        ## dernière couche
        z4 = nn.Linear(a3,self.w4)
        z4 = nn.AddBias(z4, self.b4)
        return z4

    def get_loss(self, x: nn.Constant, y: nn.Constant) -> nn.Node:
        """
        Computes the loss for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
            y: a node with shape (batch_size x 1), containing the true y-values
                to be used for training
        Returns: a loss node
        """
        "*** TODO: COMPLETE HERE FOR QUESTION 2 ***"
        return nn.SquareLoss(self.run(x) , y)

    def train(self, dataset: RegressionDataset) -> None:
        """
        Trains the model.
        """
        "*** TODO: COMPLETE HERE FOR QUESTION 2 ***"
        nb_batch = 40
        batch_size = int(dataset.x.shape[0] / nb_batch)
        learning_rate = -0.85
        epoch = 0 
        batch = 0
        loss_tol = 0.02
        loss_epoch = 0
        for x, y in dataset.iterate_forever(batch_size):
            batch += 1
            loss = self.get_loss(x,y)
            loss_epoch += nn.as_scalar(loss)
            grad_w1, grad_b1, grad_w2, grad_b2 = nn.gradients(loss, [self.w1, self.b1, self.w2, self.b2])
            try:
                self.w1.update(grad_w1, learning_rate)
                self.w2.update(grad_w2, learning_rate)
                self.b1.update(grad_b1, learning_rate)
                self.b2.update(grad_b2, learning_rate)
            except: 
                break
            ## test if we finish or not
            if batch == nb_batch: 
                epoch += 1
                batch = 0
                train_loss = loss_epoch/nb_batch
                loss_epoch = 0
                print(f"================ Epoch {epoch} ================")
                print(f"Training loss : {train_loss}")
                if train_loss < loss_tol:
                    print("********************************** Training finished **********************************")
                    break 
                

class DigitClassificationModel(object):
    """
    A model for handwritten digit classification using the MNIST dataset.

    Each handwritten digit is a 28x28 pixel grayscale image, which is flattened
    into a 784-dimensional vector for the purposes of this model. Each entry in
    the vector is a floating point number between 0 and 1.

    The goal is to sort each digit into one of 10 classes (number 0 through 9).

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """

    def __init__(self) -> None:
        # Initialize your model parameters here
        "*** TODO: COMPLETE HERE FOR QUESTION 3 ***"

    def run(self, x: nn.Constant) -> nn.Node:
        """
        Runs the model for a batch of examples.

        Your model should predict a node with shape (batch_size x 10),
        containing scores. Higher scores correspond to greater probability of
        the image belonging to a particular class.

        Inputs:
            x: a node with shape (batch_size x 784)
        Output:
            A node with shape (batch_size x 10) containing predicted scores
                (also called logits)
        """
        "*** TODO: COMPLETE HERE FOR QUESTION 3 ***"

    def get_loss(self, x: nn.Constant, y: nn.Constant) -> nn.Node:
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 10). Each row is a one-hot vector encoding the correct
        digit class (0-9).

        Inputs:
            x: a node with shape (batch_size x 784)
            y: a node with shape (batch_size x 10)
        Returns: a loss node
        """
        "*** TODO: COMPLETE HERE FOR QUESTION 3 ***"

    def train(self, dataset: DigitClassificationDataset) -> None:
        """
        Trains the model.
        """
        "*** TODO: COMPLETE HERE FOR QUESTION 3 ***"
