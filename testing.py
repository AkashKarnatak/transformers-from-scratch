import torch
from gpt2 import GPT2Model
from bert import BertModel
from transformers import (
    GPT2Tokenizer,
    GPT2LMHeadModel,
    BertTokenizer,
    BertModel as BertModelHF,
)
from bert import PositionalEmbedding, BertConfig
import matplotlib.pyplot as plt


def test_gpt2():
    # load tokenizer
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

    # load custom gpt2 model
    gpt = GPT2Model.from_pretrained("gpt2")
    # load gpt2 model from HF
    model = GPT2LMHeadModel.from_pretrained("gpt2")
    model.eval()

    # test
    text = "Hi, I am a language model,"
    encoded_input = tokenizer(text, return_tensors="pt")

    hf_out = model(encoded_input["input_ids"]).logits
    out = gpt(encoded_input["input_ids"])
    assert torch.abs(hf_out - out).max() < 1e-4, "Sanity check for GPT2Model failed"
    print("Sanity check for GPT2Model passed")


def test_bert():
    # load tokenizer
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

    # load custom gpt2 model
    bert = BertModel.from_pretrained("bert-base-uncased")
    # load gpt2 model from HF
    model = BertModelHF.from_pretrained("bert-base-uncased")
    model.eval()

    # test
    text = "Hi, I am a language model,"
    encoded_input = tokenizer(text, return_tensors="pt")

    hf_model_out = model(encoded_input["input_ids"])
    hf_out, hf_pool = hf_model_out.last_hidden_state, hf_model_out.pooler_output
    out, pool = bert(encoded_input["input_ids"])
    assert (
        torch.abs(hf_out - out).max() < 1e-4 and torch.abs(hf_pool - pool).max() < 1e-4
    ), "Sanity check for BertModel failed"
    print("Sanity check for BertModel passed")


def test_pos_embd():
    pos_emb = PositionalEmbedding(BertConfig())
    a = pos_emb(torch.arange(2000))
    print(a)
    plt.imshow(a.numpy())
    plt.show()


test_gpt2()
test_bert()
# test_pos_embd()
