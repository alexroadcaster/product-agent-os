import { SearchBox } from "../../features/search/SearchBox";
import { Header } from "../../widgets/header/Header";

export function HomePage() {
  return (
    <main aria-labelledby="home-title">
      <Header />
      <section>
        <h1 id="home-title">Synthetic Frontend Fixture</h1>
        <SearchBox />
      </section>
    </main>
  );
}
