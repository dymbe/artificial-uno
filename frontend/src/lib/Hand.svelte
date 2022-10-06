<script lang="ts">
    import type { CardModel } from './uno-types'
    import Card from './Card.svelte';
    export let cards: CardModel[]
</script>
<div class="hand">
    {#each cards as card}
    <Card height="90px" card={card}/>
    {/each}
</div>
<style>
    .hand {
        display: flex;
        height: 90px;
    }
</style>
