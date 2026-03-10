import os

class CoffeeShopGenerator:
    """Generates a modern, responsive landing page for a coffee shop."""

    def __init__(self, shop_name, tagline, accent_color, background_color, text_color):
        self.shop_name = shop_name
        self.tagline = tagline
        self.accent_color = accent_color
        self.background_color = background_color
        self.text_color = text_color
        self.filename = f"{self.shop_name.lower().replace(' ', '_')}_landing.html"

    def _get_css(self):
        return f"""
        :root {{
            --accent: {self.accent_color};
            --bg: {self.background_color};
            --text: {self.text_color};
        }}
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        body {{
            background-color: var(--bg);
            color: var(--text);
            line-height: 1.6;
        }}
        header {{
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=1350&q=80');
            background-size: cover;
            background-position: center;
            color: white;
            padding: 20px;
        }}
        h1 {{
            font-size: 4rem;
            margin-bottom: 1rem;
            color: var(--accent);
        }}
        p.tagline {{
            font-size: 1.5rem;
            margin-bottom: 2rem;
        }}
        .cta {{
            background-color: var(--accent);
            color: white;
            padding: 12px 30px;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
            transition: transform 0.3s ease;
        }}
        .cta:hover {{
            transform: scale(1.05);
        }}
        .menu {{
            padding: 80px 20px;
            max-width: 1000px;
            margin: 0 auto;
        }}
        .menu h2 {{
            text-align: center;
            font-size: 2.5rem;
            margin-bottom: 40px;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 30px;
        }}
        .item {{
            background: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            color: #333;
        }}
        footer {{
            text-align: center;
            padding: 40px;
            background: #222;
            color: #ccc;
        }}
        @media (max-width: 768px) {{
            h1 {{ font-size: 2.5rem; }}
        }}
        """

    def _get_html_content(self):
        css = self._get_css()
        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.shop_name} | Premium Coffee</title>
    <style>
        {css}
    </style>
</head>
<body>
    <header>
        <h1>{self.shop_name}</h1>
        <p class="tagline">{self.tagline}</p>
        <a href="#menu" class="cta">View Our Menu</a>
    </header>

    <section id="menu" class="menu">
        <h2>Today's Specials</h2>
        <div class="grid">
            <div class="item">
                <h3>Caramel Macchiato</h3>
                <p>Freshly steamed milk with vanilla-flavored syrup marked with espresso.</p>
            </div>
            <div class="item">
                <h3>Cold Brew</h3>
                <p>Slow-steeped in cool water for 20 hours for a super smooth taste.</p>
            </div>
            <div class="item">
                <h3>Nitro Cold Brew</h3>
                <p>Our small-batch cold brew infused with nitrogen for a velvety texture.</p>
            </div>
        </div>
    </section>

    <footer>
        <p>&copy; 2023 {self.shop_name}. All rights reserved.</p>
    </footer>
</body>
</html>
"""

    def build(self):
        try:
            content = self._get_html_content()
            with open(self.filename, "w", encoding="utf-8") as f:
                f.write(content)
            return os.path.exists(self.filename)
        except Exception:
            return False

if __name__ == "__main__":
    # Test Data 1: The Artisan Dark Roast
    shop1 = CoffeeShopGenerator(
        "Obsidian Beans", 
        "Darkness in every drop.", 
        "#d4a373", 
        "#1a1a1a", 
        "#f1f1f1"
    )
    
    # Test Data 2: Minimalist Light Cafe
    shop2 = CoffeeShopGenerator(
        "The White Mug", 
        "Pure. Simple. Essential.", 
        "#6b705c", 
        "#f8f9fa", 
        "#212529"
    )
    
    # Test Data 3: Vibrant Modern Spot
    shop3 = CoffeeShopGenerator(
        "Neon Espresso", 
        "Electric energy to start your day.", 
        "#ff006e", 
        "#ffffff", 
        "#000000"
    )

    # Execution and Verification
    success1 = shop1.build()
    success2 = shop2.build()
    success3 = shop3.build()

    if all([success1, success2, success3]):
        print("Landing Page construction complete")
    else:
        print("Error: Construction failed.")

<ctrl63>
