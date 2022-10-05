<script lang="ts">
    import { onMount } from "svelte";
    import { createUnoStateStore } from "./lib/uno-state-store";
    import type { UnoState } from "./lib/uno-types";
    import Hand from "./lib/Hand.svelte";
    import Card from "./lib/Card.svelte";

    let state: UnoState | undefined;

    onMount(() => {
        const store = createUnoStateStore();

        store.subscribe(newState => {
            state = newState;
        });

        return store.close;
    });
</script>
<main>
    {#if state}
    <div class="hands">
        {#each state.hands as cards, i}
        <div class="agent-info">
            <div>{state.aliases[i]}</div>
            <div>Score: <span class="score">{state.scores[i]}</span></div>
        </div>
        <Hand cards={cards}/>
        {/each}
    </div>
    <div class="right-side">
        <Card height="180px" card={state.topCard}/>
    </div>
    {/if}
</main>
<style>
    main {
        display: flex;
    }

    .hands {
        display: grid;
        width: 80%;
        grid-template-columns: min-content minmax(0, 1fr);
        column-gap: 16px;
        align-items: center;
    }

    .agent-info {
        font-size: 1.5em;
        white-space: nowrap;
    }

    .score {
        display: inline-block;
        text-align: end;
        width: 1.5em;
    }

    .right-side {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 20%;
    }
</style>
