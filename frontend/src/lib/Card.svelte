<script lang="ts">
    import { ColorEnum, SignEnum, type CardModel } from './uno-types'
    import Zero from '../assets/icons/zero.svelte'
    import One from '../assets/icons/one.svelte'
    import Two from '../assets/icons/two.svelte'
    import Three from '../assets/icons/three.svelte'
    import Four from '../assets/icons/four.svelte'
    import Five from '../assets/icons/five.svelte'
    import Six from '../assets/icons/six.svelte'
    import Seven from '../assets/icons/seven.svelte'
    import Eight from '../assets/icons/eight.svelte'
    import Nine from '../assets/icons/nine.svelte'
    import Skip from '../assets/icons/skip.svelte'
    import Reverse from '../assets/icons/reverse.svelte'
    import DrawTwo from '../assets/icons/draw-two.svelte'
    import DrawFour from '../assets/icons/draw-four.svelte'
    import ChangeColor from '../assets/icons/change-color.svelte'

    export let card: CardModel
    export let height: string | undefined = undefined
    export let width: string | undefined = undefined

    function getCardComponent(sign: SignEnum) {
        switch (sign) {
            case SignEnum.Enum.ZERO: return Zero
            case SignEnum.Enum.ONE: return One
            case SignEnum.Enum.TWO: return Two
            case SignEnum.Enum.THREE: return Three
            case SignEnum.Enum.FOUR: return Four
            case SignEnum.Enum.FIVE: return Five
            case SignEnum.Enum.SIX: return Six
            case SignEnum.Enum.SEVEN: return Seven
            case SignEnum.Enum.EIGHT: return Eight
            case SignEnum.Enum.NINE: return Nine
            case SignEnum.Enum.SKIP: return Skip
            case SignEnum.Enum.REVERSE: return Reverse
            case SignEnum.Enum.DRAW_TWO: return DrawTwo
            case SignEnum.Enum.DRAW_FOUR: return DrawFour
            case SignEnum.Enum.CHANGE_COLOR: return ChangeColor
            default: throw Error("Unrecognized sign")
        }
    }

    function getCssHexColor(color: ColorEnum | undefined) {
        switch (color) {
            case ColorEnum.Enum.RED: return "#f55"
            case ColorEnum.Enum.GREEN: return "#5a5"
            case ColorEnum.Enum.BLUE: return "#55f"
            case ColorEnum.Enum.YELLOW: return "#fa0"
            default: return undefined
        }
    }

    $: component = getCardComponent(card.sign)
    $: color = getCssHexColor(card.color)
</script>
<svelte:component this={component} color={color} height={height} width={width}/>
