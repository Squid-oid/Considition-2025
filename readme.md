# Considition 2025 Hackaton
My submitted code for the Considition 2025 event. The goal of the event was to efficiently suggest charging locations to customers based on the customers location, destination, charging level, travel time and preferences.

## My Thought Process and Code
My final solution suggests customers to charge at the charging location which minimally disturbs their route, and to charge just enough to make it to their destination, with a small
buffer and minimal charge in order to generate score from even drivers who had adequate charge. Sadly this solution does not take into account the potential for charging more, the 
level of free energy in the grid, brownouts, the customer preference or even other customers. 

My original idea was to predict, in turn, conditional on all previously allocated charging events the maximally scoring set of instructions for a given customer, then loop over all 
customers over and over until no more improvements can be found somewhat like a Gibbs sampler. After fighting the API for a while I gave up on this idea.

The path finding is handled in G_Map, which holds the map state and provides handy acsess to customer information, node information and distances between nodes. consiStarter.ipynb 
contains all of the running logic, where each customer is, at departure, assigned a charger, and if that single charge won't cover the journey creates a second delayed charging event
to send to the customer (in a very bad way, which I suspect fails almost all of the time since the pitch isn't actually delayed until post first charge, just a fixed delay...). My initial exploration of the data is in initial.ipynb, where we also show two methods of plotting out the map.

## Conclusion
All in all, while I finished 24th, which was far from the leaderboard, but seeing as this is my first hackathon I'm happy to have something submitted, and learned a good deal about
coding under time pressure so I think next time I can do mcuh better! 

Thank you so much to Considition for hosting this event, and to all of the other teams who have chosen to host their code, for providing such a fantastic learning opportunity.