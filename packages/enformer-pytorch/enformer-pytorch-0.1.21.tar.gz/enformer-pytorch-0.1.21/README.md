<img src="./enformer.png" width="450px"></img>

## Enformer - Pytorch

Implementation of <a href="https://deepmind.com/blog/article/enformer">Enformer</a>, Deepmind's attention network for predicting gene expression, in Pytorch. This repository also contains the means to fine tune pretrained models for your downstream tasks. The original tensorflow sonnet code can be found <a href="https://github.com/deepmind/deepmind-research/tree/master/enformer">here</a>.

## Install

```bash
$ pip install enformer-pytorch
```

## Usage

```python
import torch
from enformer_pytorch import Enformer

model = Enformer(
    dim = 1536,
    depth = 11,
    heads = 8,
    output_heads = dict(human = 5313, mouse = 1643),
    target_length = 896,
)

seq = torch.randint(0, 4, (1, 196_608)) # for ACGT, in that order
output = model(seq)

output['human'] # (1, 896, 5313)
output['mouse'] # (1, 896, 1643)
```

You can also directly pass in the sequence as one-hot encodings, which must be float values

```python
import torch
import torch.nn.functional as F
from enformer_pytorch import Enformer

model = Enformer(
    dim = 1536,
    depth = 11,
    heads = 8,
    output_heads = dict(human = 5313, mouse = 1643),
    target_length = 896,
)

seq = torch.randint(0, 4, (1, 196_608))
one_hot = F.one_hot(seq, num_classes = 4).float()

output = model(one_hot)

output['human'] # (1, 896, 5313)
output['mouse'] # (1, 896, 1643)
```

Finally, one can fetch the embeddings, for fine-tuning and otherwise, by setting the `return_embeddings` flag to be `True` on forward

```python
import torch
import torch.nn.functional as F
from enformer_pytorch import Enformer

model = Enformer(
    dim = 1536,
    depth = 11,
    heads = 8,
    output_heads = dict(human = 5313, mouse = 1643),
    target_length = 896,
)

seq = torch.randint(0, 4, (1, 196_608))
one_hot = F.one_hot(seq, num_classes = 4).float()

output, embeddings = model(one_hot, return_embeddings = True)

embeddings # (1, 896, 3072)
```

For training, you can directly pass the head and target in to get the poisson loss

```python
import torch
from enformer_pytorch import Enformer

model = Enformer(
    dim = 1536,
    depth = 11,
    heads = 8,
    output_heads = dict(human = 5313, mouse = 1643),
    target_length = 200,
).cuda()

seq = torch.randint(0, 4, (196_608 // 2,)).cuda()
target = torch.randn(200, 5313).cuda()

loss = model(
    seq,
    head = 'human',
    target = target
)

loss.backward()

# after much training

corr_coef = model(
    seq,
    head = 'human',
    target = target,
    return_corr_coef = True
)

corr_coef # pearson R, used as a metric in the paper
```

## Pretrained Model

To use a pretrained model (may not be of the same quality as the one in the paper yet), first install `gdown`

```bash
$ pip install gdown
```

Then

```python
from enformer_pytorch import load_pretrained_model

model = load_pretrained_model('preview')

# do your fine-tuning
```

You can also load, with overriding of the `target_length` parameter, if you are working with shorter sequence lengths

```python
from enformer_pytorch import load_pretrained_model

model = load_pretrained_model('preview', target_length = 128, dropout_rate = 0.1)

# do your fine-tuning
```

You can also define the model externally, and then load the pretrained weights by passing it into `load_pretrained_model`

```python
from enformer_pytorch import Enformer, load_pretrained_model

enformer = Enformer(dim = 1536, depth = 11, target_length = 128, dropout_rate = 0.1)

load_pretrained_model('preview', model = enformer)

# use enformer
```

## Fine-tuning

This repository will also allow for easy fine-tuning of Enformer.

Fine-tuning on new tracks

```python
import torch
from enformer_pytorch import Enformer
from enformer_pytorch.finetune import HeadAdapterWrapper

enformer = Enformer(
    dim = 1536,
    depth = 1,
    heads = 8,
    target_length = 200,
)

model = HeadAdapterWrapper(
    enformer = enformer,
    num_tracks = 128
).cuda()

seq = torch.randint(0, 4, (1, 196_608 // 2,)).cuda()
target = torch.randn(1, 200, 128).cuda()  # 128 tracks

loss = model(seq, target = target)
loss.backward()
```

Finetuning on contextual data (cell type, transcription factor, etc)

```python
import torch
from enformer_pytorch import Enformer
from enformer_pytorch.finetune import ContextAdapterWrapper

enformer = Enformer(
    dim = 1536,
    depth = 1,
    heads = 8,
    target_length = 200,
)

model = ContextAdapterWrapper(
    enformer = enformer,
    context_dim = 1024
).cuda()

seq = torch.randint(0, 4, (1, 196_608 // 2,)).cuda()

target = torch.randn(1, 200, 4).cuda()  # 4 tracks
context = torch.randn(4, 1024).cuda()   # 4 contexts for the different 'tracks'

loss = model(
    seq,
    context = context,
    target = target
)

loss.backward()
```

Finally, there is also a way to use attention aggregation from a set of context embeddings (or a single context embedding). Simply use the `ContextAttentionAdapterWrapper`

```python
import torch
from enformer_pytorch import Enformer
from enformer_pytorch.finetune import ContextAttentionAdapterWrapper

enformer = Enformer(
    dim = 1536,
    depth = 1,
    heads = 8,
    target_length = 200,
)

model = ContextAttentionAdapterWrapper(
    enformer = enformer,
    context_dim = 1024,
    heads = 8,              # number of heads in the cross attention
    dim_head = 64           # dimension per head
).cuda()

seq = torch.randint(0, 4, (1, 196_608 // 2,)).cuda()

target = torch.randn(1, 200, 4).cuda()      # 4 tracks
context = torch.randn(4, 16, 1024).cuda()   # 4 contexts for the different 'tracks', each with 16 tokens

context_mask = torch.ones(4, 16).bool().cuda() # optional context mask, in example, include all context tokens

loss = model(
    seq,
    context = context,
    context_mask = context_mask,
    target = target
)

loss.backward()
```

## Appreciation

Special thanks goes out to <a href="https://www.eleuther.ai/">EleutherAI</a> for providing the resources to retrain the model in an acceptable amount of time

## Todo

- [x] script to load weights from trained tensorflow enformer model to pytorch model
- [x] add loss wrapper with poisson loss
- [x] move the metrics code over to pytorch as well
- [x] train enformer model
- [x] build context manager for fine-tuning with unfrozen enformer but with frozen batchnorm
- [x] allow for plain fine-tune with fixed static context
- [x] allow for fine tuning with only unfrozen layernorms (technique from fine tuning transformers)
- [ ] add to EleutherAI huggingface

## Citations

```bibtex
@article {Avsec2021.04.07.438649,
    author  = {Avsec, {\v Z}iga and Agarwal, Vikram and Visentin, Daniel and Ledsam, Joseph R. and Grabska-Barwinska, Agnieszka and Taylor, Kyle R. and Assael, Yannis and Jumper, John and Kohli, Pushmeet and Kelley, David R.},
    title   = {Effective gene expression prediction from sequence by integrating long-range interactions},
    elocation-id = {2021.04.07.438649},
    year    = {2021},
    doi     = {10.1101/2021.04.07.438649},
    publisher = {Cold Spring Harbor Laboratory},
    URL     = {https://www.biorxiv.org/content/early/2021/04/08/2021.04.07.438649},
    eprint  = {https://www.biorxiv.org/content/early/2021/04/08/2021.04.07.438649.full.pdf},
    journal = {bioRxiv}
}
```
