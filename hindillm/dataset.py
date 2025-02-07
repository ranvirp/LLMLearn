from datasets import load_dataset

ds = load_dataset("algohype/hindi-english-iitb")
ds.save_to_disk('hindi-english-iitb')