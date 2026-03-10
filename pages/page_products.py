import flet as ft
from ui.theme import (
    ACCENT_PRIMARY,
    COLOR_DANGER,
    COLOR_WARNING,
    COLOR_SUCCESS,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    SURFACE_DARK,
    BORDER_DEFAULT,
)
from ui.components import (
    build_card,
    build_stat_card,
    build_page_header,
    build_data_table,
    build_action_button,
)
from data.constants import ALL_PRODUCTS


def build_products_page(flet_page: ft.Page):
    number_of_in_stock_products = sum(
        1 for product in ALL_PRODUCTS if product["stock"] > 0
    )
    number_of_low_stock_products = sum(
        1 for product in ALL_PRODUCTS if 0 < product["stock"] < product["reorder"]
    )
    number_of_out_of_stock_products = sum(
        1 for product in ALL_PRODUCTS if product["stock"] == 0
    )

    def determine_stock_color(product_entry):
        """Returns the appropriate color for a stock value based on threshold."""
        if product_entry["stock"] == 0:
            return COLOR_DANGER
        if product_entry["stock"] < product_entry["reorder"]:
            return COLOR_WARNING
        return COLOR_SUCCESS

    product_table_rows = [
        ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(product["id"], color=TEXT_SECONDARY, size=12)),
                ft.DataCell(
                    ft.Text(
                        product["name"],
                        color=TEXT_PRIMARY,
                        size=13,
                        weight=ft.FontWeight.W_500,
                    )
                ),
                ft.DataCell(
                    ft.Text(product["category"], color=TEXT_SECONDARY, size=12)
                ),
                ft.DataCell(
                    ft.Text(
                        str(product["stock"]),
                        color=determine_stock_color(product),
                        size=13,
                        weight=ft.FontWeight.W_600,
                    )
                ),
                ft.DataCell(
                    ft.Text(f'₹{product["price"]:,.2f}', color=TEXT_PRIMARY, size=13)
                ),
                ft.DataCell(
                    ft.Text(product["supplier"], color=TEXT_SECONDARY, size=12)
                ),
                ft.DataCell(
                    ft.Row(
                        [
                            ft.IconButton(
                                ft.Icons.EDIT,
                                icon_color=ACCENT_PRIMARY,
                                icon_size=16,
                                tooltip="Edit",
                            ),
                            ft.IconButton(
                                ft.Icons.DELETE,
                                icon_color=COLOR_DANGER,
                                icon_size=16,
                                tooltip="Delete",
                            ),
                        ],
                        spacing=0,
                    )
                ),
            ]
        )
        for product in ALL_PRODUCTS
    ]

    search_and_filter_row = ft.Row(
        [
            ft.TextField(
                hint_text="Search products...",
                prefix_icon=ft.Icons.SEARCH,
                bgcolor=SURFACE_DARK,
                border_color=BORDER_DEFAULT,
                focused_border_color=ACCENT_PRIMARY,
                color=TEXT_PRIMARY,
                hint_style=ft.TextStyle(color=TEXT_SECONDARY),
                height=42,
                expand=True,
                border_radius=10,
            ),
            ft.Dropdown(
                width=160,
                height=42,
                options=[
                    ft.dropdown.Option("All Categories"),
                    ft.dropdown.Option("Electronics"),
                    ft.dropdown.Option("Furniture"),
                    ft.dropdown.Option("Lighting"),
                ],
                value="All Categories",
                bgcolor=SURFACE_DARK,
                border_color=BORDER_DEFAULT,
                color=TEXT_PRIMARY,
                border_radius=10,
            ),
        ],
        spacing=12,
    )

    products_table_card = build_card(
        ft.Column(
            [
                search_and_filter_row,
                ft.Container(height=12),
                ft.Column(
                    [
                        build_data_table(
                            column_labels=[
                                "ID",
                                "Name",
                                "Category",
                                "Stock",
                                "Price",
                                "Supplier",
                                "Actions",
                            ],
                            table_rows=product_table_rows,
                        )
                    ],
                    scroll=ft.ScrollMode.AUTO,
                ),
            ],
            spacing=0,
        )
    )

    return ft.Column(
        [
            build_page_header(
                header_title="Products Management",
                header_subtitle="Manage your product catalog",
                header_icon=ft.Icons.INVENTORY,
                action_buttons=[build_action_button("Add Product", ft.Icons.ADD)],
            ),
            ft.Container(height=20),
            ft.ResponsiveRow(
                [
                    ft.Column(
                        [
                            build_stat_card(
                                ft.Icons.INVENTORY,
                                "Total Products",
                                len(ALL_PRODUCTS),
                                None,
                                ACCENT_PRIMARY,
                            )
                        ],
                        col={"xs": 6, "md": 3},
                    ),
                    ft.Column(
                        [
                            build_stat_card(
                                ft.Icons.CHECK_CIRCLE,
                                "In Stock",
                                number_of_in_stock_products,
                                None,
                                COLOR_SUCCESS,
                            )
                        ],
                        col={"xs": 6, "md": 3},
                    ),
                    ft.Column(
                        [
                            build_stat_card(
                                ft.Icons.WARNING,
                                "Low Stock",
                                number_of_low_stock_products,
                                None,
                                COLOR_WARNING,
                            )
                        ],
                        col={"xs": 6, "md": 3},
                    ),
                    ft.Column(
                        [
                            build_stat_card(
                                ft.Icons.CANCEL,
                                "Out of Stock",
                                number_of_out_of_stock_products,
                                None,
                                COLOR_DANGER,
                            )
                        ],
                        col={"xs": 6, "md": 3},
                    ),
                ],
                spacing=16,
            ),
            ft.Container(height=20),
            products_table_card,
        ],
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
