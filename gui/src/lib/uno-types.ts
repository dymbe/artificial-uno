import z from 'zod'

export const ColorEnum = z.enum([
    "RED",
    "GREEN",
    "BLUE",
    "YELLOW"
])
export type ColorEnum = z.infer<typeof ColorEnum>;

export const SignEnum = z.enum([
    "ZERO",
    "ONE",
    "TWO",
    "THREE",
    "FOUR",
    "FIVE",
    "SIX",
    "SEVEN",
    "EIGHT",
    "NINE",
    "SKIP",
    "REVERSE",
    "DRAW_TWO",
    "DRAW_FOUR",
    "CHANGE_COLOR",
])
export type SignEnum = z.infer<typeof SignEnum>;

export const CardModel = z.object({
    sign: SignEnum,
    color: ColorEnum.optional(),
});
export type CardModel = z.infer<typeof CardModel>;

export const UnoState = z.object({
    gameWon: z.boolean(),
    topCard: CardModel,
    hands: z.array(z.array(CardModel)),
    currentAgentIdx: z.number().int(),
    direction: z.union([z.literal(-1), z.literal(1)]),
    scores: z.array(z.number().int()),
    aliases: z.array(z.string())
});
export type UnoState = z.infer<typeof UnoState>;
