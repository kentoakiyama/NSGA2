import pickle

class Save:
    def __init__(self):
        pass

    def save_pickle(self, all_populations):
        with open('ea_cache.pkl', 'wb') as f:
            pickle.dump(all_populations, f)
    
    def load_pickle(self):
        try:
            with open('ea_cache.pkl', 'rb') as f:
                all_populations = pickle.load(f)
        except:
            all_populations = []
        return all_populations