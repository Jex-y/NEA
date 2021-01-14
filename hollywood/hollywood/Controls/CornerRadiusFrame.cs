using System;
using System.Collections.Generic;
using System.Text;
using Xamarin.Forms;

namespace hollywood.Controls
{
    public class CornerRadiusFrame : Frame
    {
        public static new readonly BindableProperty CornerRadiusProperty = 
            BindableProperty.Create(nameof(CornerRadiusFrame), typeof(CornerRadius), typeof(CornerRadiusFrame));
        public CornerRadiusFrame()
        {
            base.CornerRadius = 0;
        }

    public new CornerRadius CornerRadius
    {
        get => (CornerRadius)GetValue(CornerRadiusProperty);
        set => SetValue(CornerRadiusProperty, value);
    }
}
}
