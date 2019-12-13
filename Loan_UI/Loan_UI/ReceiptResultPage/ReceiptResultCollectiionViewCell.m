//
//  UICollectionViewCell+ReceiptResultCollectiionViewCell.m
//  Loan_UI
//
//  Created by MillionBenjamin on 2019/12/13.
//  Copyright © 2019 中山大学. All rights reserved.
//


#import "ReceiptResultCollectiionViewCell.h"
@interface  ReceiptResultCollectiionViewCell() {
    NSInteger itemWidth;
}

@end


@implementation ReceiptResultCollectiionViewCell

- (id)initWithFrame:(CGRect)frame {
    self = [super initWithFrame:frame];
    if (self)
    {
        [self addSubview:self.item1];
        [self addSubview:self.item2];
        [self addSubview:self.item3];
        [self addSubview:self.item4];
        [self addSubview:self.item5];
    }
    [self addSubview:self.item1];
    [self addSubview:self.item2];
    [self addSubview:self.item3];
    [self addSubview:self.item4];
    [self addSubview:self.item5];
    return self;
}

- (UILabel *)item1 {
    if(_item1 == nil) {
        _item1 = [[UILabel alloc] init];
        itemWidth = 200;
        _item1.frame = CGRectMake(20, 0,  itemWidth * 2, 40);
        //[_item1 setText: @"公司名称：A"];
        [_item1 setFont: [UIFont systemFontOfSize: 23]];
        [_item1 setTextColor: [UIColor blackColor]];
        
        
        //_item1.backgroundColor = [UIColor blueColor];
    }
    return _item1;
}


- (UILabel *)item2 {
    if(_item2 == nil) {
        _item2 = [[UILabel alloc] init];
        //itemWidth = 200;
        _item2.frame = CGRectMake(20, 35,  itemWidth * 2, 40);
        //[_item2 setText: @"???"];
        [_item2 setFont: [UIFont systemFontOfSize: 23]];
        [_item2 setTextColor: [UIColor blackColor]];
        
        
        //_item2.backgroundColor = [UIColor blueColor];
    }
    return _item2;
}


- (UILabel *)item3 {
    if(_item3 == nil) {
        _item3 = [[UILabel alloc] init];
        //itemWidth = 200;
        _item3.frame = CGRectMake(20, 70,  itemWidth * 2, 40);
        //[_item3 setText: @"公司名称：A"];
        [_item3 setFont: [UIFont systemFontOfSize: 23]];
        [_item3 setTextColor: [UIColor blackColor]];
        
        
        //_item3.backgroundColor = [UIColor blueColor];
    }
    return _item3;
}


- (UILabel *)item4 {
    if(_item4 == nil) {
        _item4 = [[UILabel alloc] init];
        itemWidth = 200;
        _item4.frame = CGRectMake(20, 105,  itemWidth, 40);
        //[_item4 setText: @"公司名称：A"];
        [_item4 setFont: [UIFont systemFontOfSize: 23]];
        [_item4 setTextColor: [UIColor blackColor]];

        
        //_item4.backgroundColor = [UIColor blueColor];
    }
    return _item4;
}


- (UILabel *)item5 {
    if(_item5 == nil) {
        _item5 = [[UILabel alloc] init];
        itemWidth = 200;
        _item5.frame = CGRectMake(20, 140,  itemWidth, 40);
        //[_item5 setText: @"公司名称：A"];
        [_item5 setFont: [UIFont systemFontOfSize: 23]];
        [_item5 setTextColor: [UIColor blackColor]];
    
        
        //_item5.backgroundColor = [UIColor blueColor];
    }
    return _item5;
}



@end


