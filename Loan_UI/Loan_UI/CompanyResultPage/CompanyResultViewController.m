//
//  UICollectionViewController+CompanyResultViewController.m
//  Loan_UI
//
//  Created by MillionBenjamin on 2019/12/13.
//  Copyright © 2019 中山大学. All rights reserved.
//

#import "CompanyResultViewController.h"
#import "AppDelegate.h"
#import "Masonry.h"
#import "AFNetworking.h"

@interface CompanyResultViewController () {
    NSInteger itemWidth;
}


@end

@implementation CompanyResultViewController


- (void)viewDidLoad {
    [super viewDidLoad];
    
    [self.view addSubview: self.item1];
    [self.view addSubview: self.item2];
    [self.view addSubview: self.item3];
    [self.view addSubview: self.item4];
    [self.view addSubview: self.item5];
    
    //inset distance to (top, left, bottom, right)
    /*
    UIEdgeInsets inset_title = UIEdgeInsetsMake(200, 100, 600, 100);
    [self.item1 mas_makeConstraints:^(MASConstraintMaker *make){
        make.edges.equalTo(self.view).with.insets(inset_title);
    }];
     */
    
}


- (UILabel *)item1 {
    if(_item1 == nil) {
        _item1 = [[UILabel alloc] init];
        itemWidth = 200;
        _item1.frame = CGRectMake(self.view.frame.size.width / 2 - itemWidth / 2, 280,  itemWidth * 2, 40);
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
        _item2.frame = CGRectMake(self.view.frame.size.width / 2 - itemWidth / 2, 320,  itemWidth * 2, 40);
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
        _item3.frame = CGRectMake(self.view.frame.size.width / 2 - itemWidth / 2, 360,  itemWidth * 2, 40);
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
        _item4.frame = CGRectMake(self.view.frame.size.width / 2 - itemWidth / 2, 400,  itemWidth, 40);
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
        _item5.frame = CGRectMake(self.view.frame.size.width / 2 - itemWidth / 2, 440,  itemWidth, 40);
        //[_item5 setText: @"公司名称：A"];
        [_item5 setFont: [UIFont systemFontOfSize: 23]];
        [_item5 setTextColor: [UIColor blackColor]];
    
        
        //_item5.backgroundColor = [UIColor blueColor];
    }
    return _item5;
}



@end


