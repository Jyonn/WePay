import { SellerfrontendPage } from './app.po';

describe('sellerfrontend App', () => {
  let page: SellerfrontendPage;

  beforeEach(() => {
    page = new SellerfrontendPage();
  });

  it('should display welcome message', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('Welcome to app!!');
  });
});
