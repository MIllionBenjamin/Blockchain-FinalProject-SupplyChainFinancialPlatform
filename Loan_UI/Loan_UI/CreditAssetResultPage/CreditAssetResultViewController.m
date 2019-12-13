//
//  UIViewController+CreditAssetResultViewController.m
//  Loan_UI
//
//  Created by MillionBenjamin on 2019/12/13.
//  Copyright © 2019 中山大学. All rights reserved.
//


#import "CreditAssetResultViewController.h"
#import "AppDelegate.h"
#import "Masonry.h"
#import "AFNetworking.h"

@interface CreditAssetResultViewController () {
    NSInteger itemWidth;
}


@end

@implementation CreditAssetResultViewController


- (void)viewDidLoad {
    [super viewDidLoad];
    [self.view addSubview: self.participantLabel];
    [self.view addSubview: self.amountLabel];

    
    //inset distance to (top, left, bottom, right)
    /*
    UIEdgeInsets inset_title = UIEdgeInsetsMake(200, 100, 600, 100);
    [self.amountLabel mas_makeConstraints:^(MASConstraintMaker *make){
        make.edges.equalTo(self.view).with.insets(inset_title);
    }];
     */
    
}

- (UILabel *)participantLabel {
    if(_participantLabel == nil) {
        _participantLabel = [[UILabel alloc] init];
        itemWidth = 200;
        _participantLabel.frame = CGRectMake(0, 280,  itemWidth * 2, 40);
        //[_participantLabel setText: @"???"];
        [_participantLabel setFont: [UIFont systemFontOfSize: 23]];
        [_participantLabel setTextColor: [UIColor blackColor]];
        [_participantLabel setTextAlignment:NSTextAlignmentCenter];
        
        //_participantLabel.backgroundColor = [UIColor blueColor];
    }
    return _participantLabel;
}

- (UILabel *)amountLabel {
    if(_amountLabel == nil) {
        _amountLabel = [[UILabel alloc] init];
        itemWidth = 200;
        _amountLabel.frame = CGRectMake(0, 320,  self.view.frame.size.width, 40);
        //[_amountLabel setText: @"公司名称：A"];
        [_amountLabel setFont: [UIFont systemFontOfSize: 23]];
        [_amountLabel setTextColor: [UIColor blackColor]];
        [_amountLabel setTextAlignment:NSTextAlignmentCenter];
        
        //_amountLabel.backgroundColor = [UIColor blueColor];
    }
    return _amountLabel;
}





@end
