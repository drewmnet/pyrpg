class StatBlock:
    def __init__(self, stats):
        self.stats = stats
        
    def __getitem__(self, key):
        return self.stats[key]
        
if __name__ == "__main__":
    statblock = StatBlock({"agi": 11})
    
    print(statblock["agi"])
