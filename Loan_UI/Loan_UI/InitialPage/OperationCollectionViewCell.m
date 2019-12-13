//
//  UICollectionViewCell+OperationCollectionViewCell.m
//  Loan_UI
//
//  Created by MillionBenjamin on 2019/12/12.
//  Copyright © 2019 中山大学. All rights reserved.
//

#import "OperationCollectionViewCell.h"
@interface  OperationCollectionViewCell()

@end


@implementation OperationCollectionViewCell

- (id)initWithFrame:(CGRect)frame {
    self = [super initWithFrame:frame];
    if (self)
    {
        [self addSubview:self.UnitButton];
    }
    [self addSubview:self.UnitButton];
    return self;
}

- (UIButton*)UnitButton {
    if (_UnitButton == nil) {
        _UnitButton = [UIButton buttonWithType:UIButtonTypeRoundedRect];
        _UnitButton.clipsToBounds = YES;
        [_UnitButton.layer setCornerRadius:10.0];
        [_UnitButton.layer setMasksToBounds:YES];
        
        _UnitButton.frame = CGRectMake(0, 0, 200, 50);
        
        CAGradientLayer *gradientLayer = [CAGradientLayer layer];
        gradientLayer.startPoint = CGPointMake(0, 0);
        gradientLayer.endPoint = CGPointMake(1, 1);
        // 设置渐变颜色分布区间，不设置则均匀分布
        //gradientLayer.locations = @[@(0.5),@(1.0)];//渐变点
        [gradientLayer setColors:@[(id)[[UIColor systemTealColor] CGColor],(id)[[UIColor colorWithRed:0.25 green:0.07 blue:1.00 alpha:1.0] CGColor]]];//渐变数组

        gradientLayer.frame = _UnitButton.bounds;
        [_UnitButton.layer insertSublayer:gradientLayer atIndex:0];
         
        [_UnitButton setTitleColor:[UIColor whiteColor] forState:0];
        
        _UnitButton.titleLabel.font = [UIFont systemFontOfSize:20];
        
        _UnitButton.userInteractionEnabled = NO;
    }
    return _UnitButton;
}

@end
