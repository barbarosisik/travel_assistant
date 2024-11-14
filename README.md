# travel_assistant
To use Travel Assistant on Shell,

Assuming, everything downloaded in the same structure.

1. Open a terminal, go to project directory: /travel_assistant
2. Run "rasa train".
   (You should see an ouput similar to:
    Your Rasa model is trained and saved at 'models/20241114-173634-bipartite-stack.tar.gz'.)
3. Then run: "rasa run actions" And leave the terminal up and running.
4. Open a new terminal and go to the app directory.
5. Run "rasa shell".
6. And ask for travel assistance
