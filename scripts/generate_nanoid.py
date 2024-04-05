import nanoid
import nanoid_dictionary as nd

if __name__ == "__main__":
    alphabet = nd.lowercase + nd.numbers
    id = nanoid.generate(alphabet, 10)
    print(id)