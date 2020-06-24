import time
from random import Random

class TokenGenerator:
    _adjectives = [
        'aged', 'ancient', 'autumn', 'large', 'bitter', 'black', 'blue', 'bold',
        'broad', 'broken', 'calm', 'cold', 'cool', 'crimson', 'curly', 'damp',
        'dark', 'dawn', 'delicate', 'divine', 'dry', 'empty', 'falling', 'fancy',
        'flat', 'floral', 'big', 'frosty', 'gentle', 'green', 'hidden', 'holy',
        'icy', 'jolly', 'late', 'happy', 'little', 'master', 'long', 'lucky',
        'misty', 'morning', 'muddy', 'mute', 'hot', 'noisy', 'tasty', 'old',
        'orange', 'patient', 'plain', 'polished', 'proud', 'purple', 'quiet', 'rapid',
        'raspy', 'red', 'restless', 'rough', 'round', 'royal', 'shiny', 'smart',
        'shy', 'silent', 'small', 'snowy', 'soft', 'solid', 'sparkling', 'spring',
        'square', 'steep', 'still', 'summer', 'super', 'sweet', 'throbbing', 'tight',
        'tiny', 'twilight', 'wandering', 'weathered', 'white', 'wild', 'winter', 'wispy',
        'sharp', 'yellow', 'young'
    ]

    _nouns = [
        'art', 'band', 'bar', 'base', 'bird', 'block', 'boat', 'bonus',
        'bread', 'breeze', 'brook', 'bush', 'butterfly', 'cake', 'cell', 'cherry',
        'cloud', 'credit', 'darkness', 'dawn', 'dew', 'disk', 'dream', 'dust',
        'feather', 'field', 'fire', 'firefly', 'flower', 'fog', 'forest', 'frog',
        'frost', 'glade', 'glitter', 'grass', 'hall', 'hat', 'haze', 'heart',
        'hill', 'king', 'lab', 'lake', 'leaf', 'limit', 'math', 'meadow',
        'mode', 'moon', 'morning', 'mountain', 'mouse', 'mud', 'night', 'paper',
        'pine', 'poetry', 'pond', 'queen', 'rain', 'recipe', 'dog', 'rice',
        'river', 'salad', 'scene', 'sea', 'shadow', 'shape', 'silence', 'sky',
        'smoke', 'snow', 'snowflake', 'sound', 'star', 'sun', 'sun', 'sunset',
        'surf', 'term', 'thunder', 'tooth', 'tree', 'truth', 'union', 'unit',
        'violet', 'voice', 'water', 'waterfall', 'wave', 'wildflower', 'wind', 'wood'
    ]

    def __init__(self):
        seed = "pandemic" + str(time.time())
        self.random = Random(seed)

    def generate(self):
        adjective = self.random.choice(self._adjectives)
        noun = self.random.choice(self._nouns)
        token = ''.join(self.random.choice('0123456789abcedf') for _ in range(4))
        sections = [adjective, noun, token]
        return '-'.join(sections)

    
