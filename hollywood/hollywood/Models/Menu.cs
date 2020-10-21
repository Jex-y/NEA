using System;
using System.Collections.Generic;
using System.Text;

namespace hollywood.Models
{
    class Menu
    {
        MenuHandle handle { get; }
        List<MenuHandle> submenus { get; }
        List<Item> items { get; }
    }
}
