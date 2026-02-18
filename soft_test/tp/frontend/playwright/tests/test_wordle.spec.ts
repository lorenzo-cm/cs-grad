import { test, expect } from '@playwright/test';

test.beforeEach(async ({ page }) => {
  await page.goto('http://localhost:3000');
});


test('should display title on load', async ({ page }) => {
  await expect(page.getByText('Wordle')).toBeVisible();
});


test('should display virtual keyboard with all keys', async ({ page }) => {
  const keys = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'];
  for (const key of keys) {
    await expect(page.getByRole('button', { name: key, exact: true })).toBeVisible();
  }
});


test('should display virtual keyboard with enter key', async ({ page }) => {
  const key = 'ENTER'
  
  await expect(page.getByRole('button', { name: key, exact: true })).toBeVisible();
});


test('should type and submit a valid word', async ({ page }) => {
  for (const letter of ['P', 'I', 'A', 'N', 'O']) {
    await page.getByRole('button', { name: letter, exact: true }).click();
  }
  await page.getByRole('button', { name: 'ENTER', exact: true }).click();

  await expect(page.getByText('Tentativa 2 de 6')).toBeVisible();
});


test('should show error for invalid word', async ({ page }) => {
  for (const letter of ['J', 'U', 'L', 'I', 'A']) {
    await page.getByRole('button', { name: letter, exact: true }).click();
  }
  await page.getByRole('button', { name: 'ENTER', exact: true }).click();

  await expect(page.getByText(/not in the word list/i)).toBeVisible();
});


test('should not allow repeated words', async ({ page }) => {
  for (let i = 0; i < 2; i++) {
    for (const letter of ['P', 'I', 'A', 'N', 'O']) {
      await page.getByRole('button', { name: letter, exact: true }).click();
    }
    await page.getByRole('button', { name: 'ENTER', exact: true }).click();
  }

  await expect(page.getByText(/Palavra já tentada/i)).toBeVisible();
});


test('should end game after 6 attempts with fail', async ({ page }) => {
  const words = ['PIANO', 'AJUDA', 'HIATO', 'COBRA', 'ARROZ', 'JUSTO'];
  for (const word of words) {
    for (const letter of word) {
      await page.getByRole('button', { name: letter, exact: true }).click();
    }
    await page.getByRole('button', { name: 'ENTER', exact: true }).click();
    await page.waitForTimeout(200); // wait animations
  }

  await expect(page.getByText(/Fim de jogo/i)).toBeVisible();
});


test('should restart game after losing', async ({ page }) => {
  const words = ['PIANO', 'AJUDA', 'HIATO', 'COBRA', 'ARROZ', 'JUSTO'];
  for (const word of words) {
    for (const letter of word) {
      await page.getByRole('button', { name: letter, exact: true }).click();
    }
    await page.getByRole('button', { name: 'ENTER', exact: true }).click();
    await page.waitForTimeout(200);
  }

  await page.getByRole('button', { name: /jogar novamente/i }).click();
  await expect(page.getByText('Tentativa 1 de 6')).toBeVisible();
});


test('should increment attempt counter after submitting', async ({ page }) => {
  const word = 'PIANO';
  for (const letter of word) {
    await page.getByRole('button', { name: letter, exact: true }).click();
  }
  await page.getByRole('button', { name: 'ENTER', exact: true }).click();

  await expect(page.getByText('Tentativa 2 de 6')).toBeVisible();
});


test('should update key colors after guess', async ({ page }) => {
  const words = ['PIANO', 'AJUDA', 'EXATO']; // all vowels, one has got to lit up green
  for (const word of words) {
    for (const letter of word) {
      await page.getByRole('button', { name: letter, exact: true }).click();
    }
    await page.getByRole('button', { name: 'ENTER', exact: true }).click();
    await page.waitForTimeout(200);
  }

  const button = await page.getByRole('button', { name: 'A', exact: true });
  const color = await button.evaluate(node => getComputedStyle(node).backgroundColor);
  expect(color).not.toBe('rgb(75, 75, 75)'); // not neutral gray
});