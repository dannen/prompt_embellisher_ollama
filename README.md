# prompt_embellisher_ollama
This is a node for ComfyUI that integrates a locally installed ollama service to embellish your prompts in your ComfyUI workflow.

Add this into comfy/ComfyUI/custom_nodes/

## You'll see two text boxes:
The top one is your base prompt.  It can be whatever you'd like.
The bottom one is what your embellish prompt. It is fed to ollama in order to embellish the first prompt.

e.g.
```
Base Prompt:
A large red car parked in a city.
Embellish Prompt:
new york city, trash, sunset
```

This generated the following text:
```
A large red car parked in a city. 
( In the heart of New York City, as the sun dipped low behind the towering skyline,
casting its golden rays across a myriad of streets, the city breathed heavily,
almost as if it were alive. It was then that we saw, like a forgotten tale,
the discarded trash emerging from the shadows of old alleys, dancing in the moonlight.
Their silent song of neglect and decay echoed through the air, like whispers carried on a midnight breeze.
As the city turned into a sea of stars and neon lights, the forsaken trash became a part of its nightly splendor;
an unwelcome, but captivating melody that harmonized with the city's rhythm.
And thus, New York City, once again, painted a symphony of both beauty and tragedy,
the city's trash and glamor entwined in an unbreakable bond, as if each were meant
to find the other in this grand orchestra of life.:1.5)
```

##Below that is your modifiers

tone: a variety of options to choose from

intensity: the strength that ollama will use to adjust the prompt.

max lines: 1-10 lines of output from ollama.  More than that will eat all of your VRAM.

##llm selections
next you will see all llms that have been discovered on your local system.
You should only toggle one at a time to on.

![alt text](ComfyUI_00001_.png)
