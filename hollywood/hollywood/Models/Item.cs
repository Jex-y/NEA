using System;
using System.Collections.Generic;
using System.Text;
using Xamarin.Forms;

namespace hollywood.Models
{
    class Item
    {
        Guid ID { get; }
        string Name { get; }
        string Description { get; }
        decimal Price { get; }
        List<Tag> Tags { get; }
        Uri Image { get; }
    }
}
