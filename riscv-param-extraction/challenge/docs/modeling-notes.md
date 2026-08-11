# Modeling notes (challenge surface)

Short notes on modeling judgment, not only tooling.

## Independent parameters vs bundling

When the manual lists independent implementation choices in one sentence (e.g. cache capacity, organization, and block size), prefer **separate parameters** unless the text forces a shared constraint. Shipping one bundled parameter overclaims structure the spec does not state. This matches UDB review culture that prefers split parameters when axes are independent.

## Opaque strings vs invented enums

If the text gives no enumerable value space, prefer a minimal schema (e.g. opaque `string`) and flag SIG scoping, do not invent enums. That is a form of anti-hallucination at the **schema** layer, not only at the quote layer.

## Empty results are valid

The CSR address-mapping snippet is a negative control: fixed convention language is not optionality. Returning **zero** parameters is correct. Prompts and validators must not punish emptiness.

## Known-param bench vs corpus recall

`benchmark/` (n=15) checks mechanics on paired sources. It is **not** equal to Spring corpus adjusted recall and is **pretraining-leaky** by construction (public UDB params). Report existence/type fidelity with that caveat first.

## Holdout vs challenge

The temporal holdout pilot tests CSR-context under a frozen pin. The locked v1.2 primary is an **exploratory null** with documented guidance limitations, method evidence, not a marketing win on WARL.
